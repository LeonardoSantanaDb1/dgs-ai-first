# Prompt 02 - Implementação da Ingestão

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04  

--- 

## Objetivo

Solicitar apoio do Claude Code na implementação da etapa de ingestão do pipeline RAG.

---

## Contexto

A solução utiliza:

- Python
- ChromaDB
- sentence-transformers
- Documentos Markdown

A implementação deve:

1. Ler todos os arquivos da pasta docs.
2. Aplicar chunking.
3. Gerar embeddings.
4. Persistir os vetores no ChromaDB.
5. Salvar metadados dos documentos.

---

## Prompt Utilizado

Estou desenvolvendo o Exercício 1.3 da trilha AI First.

Contexto:

Preciso construir uma prova de conceito funcional de um pipeline RAG utilizando apenas ferramentas gratuitas e open-source.

Stack definida:

- Python
- ChromaDB
- sentence-transformers
- Modelo de embeddings: all-MiniLM-L6-v2

Estrutura atual do projeto:

pipeline-rag/
├── docs/
│   ├── FAQ-atendimento.md
│   ├── POL-001-politica-devolucao.md
│   ├── PROC-042-frete-especial-v1.md
│   ├── PROC-042-v2-frete-especial-revisado.md
│   └── SLA-2024-tabela-sla-clientes.md
│
├── src/
│   ├── ingest.py
│   ├── search.py
│   └── prompt_builder.py
│
├── chroma_db/
├── requirements.txt
└── README.md

Objetivo desta etapa:

Implementar apenas o arquivo ingest.py.

Requisitos obrigatórios:

1. Ler todos os arquivos Markdown da pasta docs.
2. Preservar o nome do documento como metadado.
3. Aplicar uma estratégia simples de chunking adequada para uma POC.
4. Gerar embeddings utilizando sentence-transformers (all-MiniLM-L6-v2).
5. Armazenar os embeddings no ChromaDB.
6. Salvar metadados contendo:
   - nome do documento
   - índice do chunk
   - conteúdo original
7. O código deve ser simples, legível e adequado para demonstração acadêmica.
8. Adicionar comentários explicando cada etapa.
9. Não utilizar LangChain.
10. Não implementar funcionalidades além do escopo da ingestão.

Antes de gerar o código:

- Analise a arquitetura proposta.
- Identifique riscos ou melhorias.
- Explique brevemente as decisões técnicas.
- Em seguida gere o código completo do ingest.py.