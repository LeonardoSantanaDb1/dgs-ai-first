"""
Pipeline de Busca — NovaTech RAG (POC)

Responsabilidade: receber uma pergunta, gerar seu embedding, consultar o ChromaDB
e retornar os top-k chunks mais similares com metadados e score de similaridade.

Uso:
  python search.py "Qual o prazo de devolução para carga perigosa?"
  python search.py "Quanto custa frete para 600kg para Manaus?" --top-k 5

Notas sobre score:
  O ChromaDB com hnsw:space=cosine retorna distância cosine (0 = idêntico).
  Para leitura mais intuitiva, o output exibe similaridade = 1 - distância,
  onde 1.0 significa correspondência perfeita e 0.0 significa sem relação.
"""

import argparse
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Configuração — deve espelhar exatamente os valores usados em ingest.py
# ---------------------------------------------------------------------------

CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"
COLLECTION_NAME = "novatech_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # mesmo modelo da ingestão — obrigatório
DEFAULT_TOP_K = 3


# ---------------------------------------------------------------------------
# Etapa 1 — Geração do embedding da pergunta
# ---------------------------------------------------------------------------

def embed_query(query: str, model: SentenceTransformer) -> list[float]:
    """
    Converte a pergunta em um vetor usando o mesmo modelo da ingestão.
    O resultado precisa estar no mesmo espaço vetorial dos chunks indexados;
    qualquer divergência de modelo tornaria a busca por similaridade inválida.
    """
    vector = model.encode(query, show_progress_bar=False)
    return vector.tolist()


# ---------------------------------------------------------------------------
# Etapa 2 — Busca no ChromaDB
# ---------------------------------------------------------------------------

def search(
    query_embedding: list[float],
    collection: chromadb.Collection,
    top_k: int,
) -> dict:
    """
    Consulta o ChromaDB com o embedding da pergunta e retorna os top-k resultados.

    O ChromaDB retorna um dict com listas paralelas:
      ids, distances, documents, metadatas — todas na mesma ordem de ranking.
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    return results


# ---------------------------------------------------------------------------
# Etapa 3 — Formatação e exibição dos resultados
# ---------------------------------------------------------------------------

def display_results(query: str, results: dict) -> None:
    """
    Exibe os resultados de forma legível para análise durante a POC.

    Para cada chunk recuperado mostra:
      - Posição no ranking
      - Documento de origem (rastreabilidade)
      - Índice do chunk no documento
      - Score de similaridade (1 - distância cosine)
      - Conteúdo completo do chunk
    """
    ids        = results["ids"][0]           # lista de IDs
    distances  = results["distances"][0]     # distância cosine (menor = mais similar)
    documents  = results["documents"][0]     # texto do chunk
    metadatas  = results["metadatas"][0]     # metadados armazenados na ingestão

    print(f"\n{'='*60}")
    print(f"Pergunta: {query}")
    print(f"{'='*60}")
    print(f"{len(ids)} chunk(s) recuperado(s)\n")

    for rank, (doc_id, distance, text, meta) in enumerate(
        zip(ids, distances, documents, metadatas), start=1
    ):
        # Converte distância cosine em score de similaridade para leitura intuitiva
        similarity = 1.0 - distance

        print(f"--- Resultado #{rank} {'─'*40}")
        print(f"  Documento  : {meta.get('doc_name', 'desconhecido')}")
        print(f"  Chunk idx  : {meta.get('chunk_index', '?')}")
        print(f"  Similaridade: {similarity:.4f}  (distância cosine: {distance:.4f})")
        print(f"  ID         : {doc_id}")
        print()
        print(f"  Conteúdo:")
        # Indenta cada linha do chunk para separar visualmente do restante do output
        for line in text.splitlines():
            print(f"    {line}")
        print()

    print("="*60)


# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Busca semântica na base de documentos NovaTech (ChromaDB).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemplos:\n"
            '  python search.py "Qual o prazo de devolução?"\n'
            '  python search.py "Frete para 600kg para Manaus" --top-k 5\n'
        ),
    )
    parser.add_argument(
        "query",
        type=str,
        help="Pergunta em linguagem natural para buscar na base de documentos.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        dest="top_k",
        help=f"Número de chunks a recuperar (padrão: {DEFAULT_TOP_K}).",
    )
    args = parser.parse_args()

    # Validação básica de top_k para evitar erros silenciosos do ChromaDB
    if args.top_k < 1:
        parser.error("--top-k deve ser >= 1.")

    print(f"[1/3] Carregando modelo '{EMBEDDING_MODEL}'...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"[2/3] Gerando embedding da pergunta...")
    query_embedding = embed_query(args.query, model)

    print(f"[3/3] Consultando ChromaDB (top-k={args.top_k})...")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(name=COLLECTION_NAME)
    results = search(query_embedding, collection, args.top_k)

    display_results(args.query, results)


if __name__ == "__main__":
    main()
