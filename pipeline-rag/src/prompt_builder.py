"""
Construtor de Prompt — NovaTech RAG (POC)

Responsabilidade: recuperar os chunks mais relevantes para uma pergunta e montar
o prompt completo (system prompt + contexto + pergunta) pronto para ser colado
manualmente no Claude ou em qualquer LLM.

Este módulo encerra o pipeline RAG de ponta a ponta:
  Pergunta → Embedding → Retrieval → Montagem de Prompt

Estrutura do contexto (estático vs dinâmico):
  ┌─────────────────────────────┐
  │  SYSTEM PROMPT  (estático)  │  Define identidade, regras e formato — não muda por query.
  ├─────────────────────────────┤
  │  CHUNKS RECUPERADOS         │  Dinâmico — varia a cada pergunta conforme o retrieval.
  │  (dinâmico, top-k)          │
  ├─────────────────────────────┤
  │  PERGUNTA DO USUÁRIO        │  Dinâmico — entrada do atendente.
  │  (dinâmico)                 │
  └─────────────────────────────┘

Uso:
  python prompt_builder.py "Qual o prazo de devolução para carga perigosa?"
  python prompt_builder.py "Frete para 600kg para Manaus" --top-k 5
  python prompt_builder.py "Qual o SLA do cliente Gold?" --show-chunks
"""

import argparse
import sys
from pathlib import Path

# Importa as funções já validadas do módulo de busca.
# Reutilizar em vez de duplicar garante que correções no retrieval se propagam aqui.
from search import embed_query, search, EMBEDDING_MODEL, CHROMA_DIR, COLLECTION_NAME, DEFAULT_TOP_K

import chromadb
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------------------------
# System Prompt — parte estática do contexto
#
# Definido como constante para deixar explícito que este bloco é versionável
# e independente da lógica de retrieval. Em produção ficaria num arquivo
# separado (ex: prompts/system_prompt_v1.txt) controlado por versionamento.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """Você é o Assistente de Atendimento da NovaTech.

Responda utilizando exclusivamente as informações presentes no contexto fornecido.

Regras obrigatórias:
- Sempre cite a fonte do documento utilizado.
- Nunca invente prazos, valores, regras ou procedimentos.
- Se a resposta não estiver presente no contexto, informe que não encontrou informação suficiente.
- Quando não houver evidência suficiente, recomende escalar para o supervisor.
- Responda em português formal e acessível.

Formato esperado da resposta:
Resposta:
[resposta objetiva]

Fonte:
[documento utilizado]

Observações:
[observações relevantes ou exceções]"""


# ---------------------------------------------------------------------------
# Etapa 1 — Extração dos chunks a partir do resultado do retrieval
# ---------------------------------------------------------------------------

def extract_chunks(results: dict) -> list[dict]:
    """
    Converte o dict bruto retornado pelo ChromaDB numa lista estruturada de chunks,
    adicionando o score de similaridade calculado a partir da distância cosine.

    Retorna lista de dicts com: text, doc_name, chunk_index, similarity.
    """
    chunks = []
    ids        = results["ids"][0]
    distances  = results["distances"][0]
    documents  = results["documents"][0]
    metadatas  = results["metadatas"][0]

    for doc_id, distance, text, meta in zip(ids, distances, documents, metadatas):
        chunks.append({
            "text":        text,
            "doc_name":    meta.get("doc_name", "desconhecido"),
            "chunk_index": meta.get("chunk_index", "?"),
            "similarity":  round(1.0 - distance, 4),   # 1.0 = idêntico, 0.0 = sem relação
        })

    return chunks


# ---------------------------------------------------------------------------
# Etapa 2 — Montagem do prompt completo
# ---------------------------------------------------------------------------

def build_prompt(query: str, chunks: list[dict]) -> str:
    """
    Monta o prompt final combinando as partes estática e dinâmica do contexto:

      1. System prompt  → define o comportamento do LLM (estático)
      2. Contexto       → chunks recuperados, cada um identificado pela sua fonte (dinâmico)
      3. Pergunta       → entrada do atendente (dinâmico)

    Delimitadores [CONTEXTO_INICIO] / [CONTEXTO_FIM] ensinam explicitamente ao LLM
    onde termina o contexto documental e começam as instruções — reduz risco de
    o modelo misturar formatação Markdown dos documentos com estrutura do prompt.
    """
    # --- Bloco de contexto: um chunk por seção, com identificação de fonte ---
    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        header = f"[Fonte {i}: {chunk['doc_name']} | chunk {chunk['chunk_index']}]"
        context_blocks.append(f"{header}\n{chunk['text']}")

    context_section = "\n\n".join(context_blocks)

    # --- Montagem final ---
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"[CONTEXTO_INICIO]\n"
        f"{context_section}\n"
        f"[CONTEXTO_FIM]\n\n"
        f"Pergunta do atendente: {query}"
    )

    return prompt


# ---------------------------------------------------------------------------
# Etapa 3 — Estimativa de tamanho do prompt
# ---------------------------------------------------------------------------

def estimate_tokens(text: str) -> int:
    """
    Estimativa simplificada: ~4 caracteres por token (regra prática para português).
    Em produção, usar tiktoken para contagem exata por modelo.
    """
    return len(text) // 4


# ---------------------------------------------------------------------------
# Exibição do diagnóstico de retrieval (opcional, ativado por --show-chunks)
# ---------------------------------------------------------------------------

def display_retrieval_diagnostics(query: str, chunks: list[dict]) -> None:
    """
    Exibe os scores de similaridade de cada chunk recuperado.
    Útil para análise crítica do pipeline sem poluir o output principal do prompt.
    """
    print("\n" + "─" * 60)
    print("DIAGNÓSTICO DE RETRIEVAL")
    print("─" * 60)
    print(f"Pergunta : {query}")
    print(f"Chunks   : {len(chunks)} recuperado(s)\n")

    for i, chunk in enumerate(chunks, start=1):
        print(f"  #{i}  similaridade={chunk['similarity']:.4f}"
              f"  |  {chunk['doc_name']}  (chunk {chunk['chunk_index']})")
        # Exibe apenas a primeira linha do chunk para manter o diagnóstico compacto
        preview = chunk["text"].splitlines()[0][:80]
        print(f"       preview: {preview}...")
        print()

    print("─" * 60 + "\n")


# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Monta o prompt RAG completo para a NovaTech — pronto para colar no Claude.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemplos:\n"
            '  python prompt_builder.py "Qual o prazo de devolução para carga perigosa?"\n'
            '  python prompt_builder.py "Frete para 600kg para Manaus" --top-k 5\n'
            '  python prompt_builder.py "Qual o SLA do cliente Gold?" --show-chunks\n'
        ),
    )
    parser.add_argument(
        "query",
        type=str,
        help="Pergunta em linguagem natural do atendente.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        dest="top_k",
        help=f"Número de chunks a recuperar (padrão: {DEFAULT_TOP_K}).",
    )
    parser.add_argument(
        "--show-chunks",
        action="store_true",
        dest="show_chunks",
        help="Exibe diagnóstico de retrieval com scores de similaridade antes do prompt.",
    )
    args = parser.parse_args()

    if args.top_k < 1:
        parser.error("--top-k deve ser >= 1.")

    # --- Retrieval ---
    print(f"[1/3] Carregando modelo '{EMBEDDING_MODEL}'...", file=sys.stderr)
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"[2/3] Gerando embedding e consultando ChromaDB (top-k={args.top_k})...", file=sys.stderr)
    query_embedding = embed_query(args.query, model)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(name=COLLECTION_NAME)
    results = search(query_embedding, collection, args.top_k)

    # --- Extração e estruturação dos chunks ---
    chunks = extract_chunks(results)

    # --- Diagnóstico opcional ---
    if args.show_chunks:
        display_retrieval_diagnostics(args.query, chunks)

    # --- Montagem do prompt ---
    print(f"[3/3] Montando prompt...", file=sys.stderr)
    prompt = build_prompt(args.query, chunks)

    # --- Estimativa de orçamento de contexto ---
    estimated_tokens = estimate_tokens(prompt)
    system_tokens = estimate_tokens(SYSTEM_PROMPT)
    print(f"\n[INFO] Prompt montado — tamanho estimado: ~{estimated_tokens} tokens", file=sys.stderr)
    print(f"[INFO] Janela GPT-4o: 128K tokens | System prompt: ~{system_tokens} tokens estáticos", file=sys.stderr)
    print(f"[INFO] Chunks dinâmicos: ~{estimated_tokens - system_tokens} tokens\n", file=sys.stderr)

    # --- Output principal: o prompt pronto para copiar ---
    # Vai para stdout separado do diagnóstico (stderr), permitindo redirecionamento:
    #   python prompt_builder.py "pergunta" > prompt.txt
    print("=" * 60)
    print("PROMPT GERADO — copie e cole no Claude:")
    print("=" * 60)
    print(prompt)
    print("=" * 60)


if __name__ == "__main__":
    main()
