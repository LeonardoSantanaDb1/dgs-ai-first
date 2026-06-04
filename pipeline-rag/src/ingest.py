"""
Pipeline de Ingestão — NovaTech RAG (POC)

Responsabilidade: ler os documentos Markdown da pasta docs/, dividir em chunks
semânticos, gerar embeddings com sentence-transformers e persistir no ChromaDB.

Estratégia de chunking:
  Divisão por seção (headers ## e ###) em vez de janela fixa de tokens.
  Documentos da NovaTech têm estrutura bem definida por headers — respeitar essas
  fronteiras semânticas evita cortar tabelas de multiplicadores de frete no meio,
  o que degradaria a qualidade do retrieval para perguntas numéricas.

  Seções que excedam MAX_CHUNK_CHARS são subdivididas por parágrafo com overlap
  de 1 parágrafo para não perder contexto nas fronteiras.
"""

import os
import re
import uuid
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

DOCS_DIR = Path(__file__).parent.parent / "docs"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"
COLLECTION_NAME = "novatech_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Tamanho máximo de um chunk em caracteres antes de subdividir por parágrafo.
# ~1.500 caracteres ≈ ~300 tokens — cabe folgado no orçamento de contexto do LLM
# e ainda preserva contexto suficiente para o modelo responder perguntas simples.
MAX_CHUNK_CHARS = 1500

# Número de parágrafos de sobreposição ao subdividir seções longas.
OVERLAP_PARAGRAPHS = 1


# ---------------------------------------------------------------------------
# Etapa 1 — Leitura dos documentos
# ---------------------------------------------------------------------------

def load_documents(docs_dir: Path) -> list[dict]:
    """Lê todos os arquivos .md do diretório e retorna lista de {filename, content}."""
    documents = []
    for path in sorted(docs_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        documents.append({
            "filename": path.name,
            "content": content,
        })
        print(f"  [lido] {path.name} ({len(content)} chars)")
    return documents


# ---------------------------------------------------------------------------
# Etapa 2 — Chunking semântico por seção
# ---------------------------------------------------------------------------

def split_into_sections(content: str) -> list[str]:
    """
    Divide o conteúdo Markdown em seções usando headers (## e ###) como delimitadores.
    O texto antes do primeiro header é tratado como uma seção de cabeçalho/metadados.
    """
    # Divide nas linhas que começam com ## ou ### (mas não #, que é o título do doc)
    parts = re.split(r"(?m)^(#{2,3} .+)$", content)

    sections = []
    current = []

    for part in parts:
        if re.match(r"^#{2,3} .+", part):
            # Inicia nova seção: persiste a acumulada e começa nova com o header
            if current:
                sections.append("\n".join(current).strip())
            current = [part]
        else:
            current.append(part)

    if current:
        sections.append("\n".join(current).strip())

    # Remove seções vazias ou só com espaços
    return [s for s in sections if s.strip()]


def subdivide_long_section(section: str, max_chars: int, overlap: int) -> list[str]:
    """
    Se uma seção exceder max_chars, subdividir por parágrafo com overlap.
    Isso preserva contexto nas fronteiras sem perder informação.
    """
    if len(section) <= max_chars:
        return [section]

    paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]
    chunks = []
    window = []
    current_len = 0

    for para in paragraphs:
        if current_len + len(para) > max_chars and window:
            chunks.append("\n\n".join(window))
            # Overlap: mantém os últimos N parágrafos na próxima janela
            window = window[-overlap:]
            current_len = sum(len(p) for p in window)

        window.append(para)
        current_len += len(para)

    if window:
        chunks.append("\n\n".join(window))

    return chunks


def chunk_document(doc: dict) -> list[dict]:
    """
    Aplica chunking semântico a um documento e retorna lista de chunks com metadados.

    Cada chunk contém:
      - chunk_id: identificador único (UUID)
      - doc_name: nome do arquivo-fonte (rastreabilidade)
      - chunk_index: posição do chunk dentro do documento
      - text: conteúdo textual do chunk
    """
    sections = split_into_sections(doc["content"])
    chunks = []
    chunk_index = 0

    for section in sections:
        # Subdivide seções longas para respeitar o orçamento de atenção do LLM
        sub_chunks = subdivide_long_section(section, MAX_CHUNK_CHARS, OVERLAP_PARAGRAPHS)

        for sub in sub_chunks:
            chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "doc_name": doc["filename"],
                "chunk_index": chunk_index,
                "text": sub,
            })
            chunk_index += 1

    return chunks


# ---------------------------------------------------------------------------
# Etapa 3 — Geração de embeddings
# ---------------------------------------------------------------------------

def generate_embeddings(chunks: list[dict], model: SentenceTransformer) -> list[list[float]]:
    """
    Gera embeddings para a lista de chunks usando o modelo sentence-transformers.
    Retorna lista de vetores na mesma ordem dos chunks.
    """
    texts = [chunk["text"] for chunk in chunks]
    # show_progress_bar=False para saída limpa em demonstrações
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


# ---------------------------------------------------------------------------
# Etapa 4 — Persistência no ChromaDB
# ---------------------------------------------------------------------------

def store_in_chromadb(
    chunks: list[dict],
    embeddings: list[list[float]],
    collection: chromadb.Collection,
) -> None:
    """
    Armazena os chunks e seus embeddings na coleção ChromaDB.

    Metadados persistidos por chunk:
      - doc_name: origem do chunk (permite filtrar por documento)
      - chunk_index: posição no documento (útil para reordenar resultados)
      - text: conteúdo original (evita busca extra para montar o prompt)
    """
    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        embeddings=embeddings,
        documents=[c["text"] for c in chunks],
        metadatas=[
            {
                "doc_name": c["doc_name"],
                "chunk_index": c["chunk_index"],
                # Armazenar o texto nos metadados é redundante com 'documents',
                # mas facilita a inspeção direta da coleção sem query de retrieval.
                "text": c["text"],
            }
            for c in chunks
        ],
    )


# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== Pipeline de Ingestão — NovaTech RAG ===\n")

    # --- Leitura ---
    print("1. Lendo documentos...")
    documents = load_documents(DOCS_DIR)
    print(f"   {len(documents)} documentos carregados.\n")

    # --- Chunking ---
    print("2. Aplicando chunking semântico por seção...")
    all_chunks: list[dict] = []
    for doc in documents:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)
        print(f"   {doc['filename']}: {len(chunks)} chunks")
    print(f"   Total: {len(all_chunks)} chunks.\n")

    # --- Embeddings ---
    print(f"3. Gerando embeddings com '{EMBEDDING_MODEL}'...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = generate_embeddings(all_chunks, model)
    print(f"   {len(embeddings)} embeddings gerados (dim={len(embeddings[0])}).\n")

    # --- ChromaDB ---
    print(f"4. Persistindo no ChromaDB em '{CHROMA_DIR}'...")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Recria a coleção para garantir reprocessamento limpo em re-execuções
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)
        print(f"   Coleção '{COLLECTION_NAME}' existente removida (reprocessamento).")

    collection = client.create_collection(
        name=COLLECTION_NAME,
        # cosine é mais adequado que l2 para comparar significado semântico de texto
        metadata={"hnsw:space": "cosine"},
    )
    store_in_chromadb(all_chunks, embeddings, collection)
    print(f"   {len(all_chunks)} chunks armazenados na coleção '{COLLECTION_NAME}'.\n")

    print("=== Ingestão concluída com sucesso. ===")


if __name__ == "__main__":
    main()
