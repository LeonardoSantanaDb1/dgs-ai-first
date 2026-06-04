# Prompt 03 - Implementação da Busca Semântica

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04  

---

## Objetivo

Solicitar apoio do Claude Code para implementar a etapa de busca semântica do pipeline RAG.

---

## Prompt Enviado ao Claude Code

Estou desenvolvendo o Exercício 1.3 da trilha AI First.

A etapa de ingestão já foi implementada e executada com sucesso.

Resultado da ingestão:

- 5 documentos processados
- 39 chunks gerados
- 39 embeddings gerados
- 39 chunks persistidos no ChromaDB
- Collection: novatech_docs

Agora preciso implementar apenas o arquivo:

src/search.py

Requisitos:

1. Receber uma pergunta via linha de comando.
2. Gerar embedding da pergunta usando sentence-transformers com o mesmo modelo da ingestão: all-MiniLM-L6-v2.
3. Conectar ao ChromaDB persistido em ./chroma_db.
4. Consultar a collection novatech_docs.
5. Recuperar os top-k chunks mais similares.
6. Exibir para cada resultado:
   - posição no ranking
   - documento de origem
   - índice do chunk
   - score/distância de similaridade
   - conteúdo do chunk
7. Permitir configurar top-k com parâmetro opcional.
8. Manter o código simples, legível e adequado para POC.
9. Não usar LangChain.
10. Não implementar funcionalidades fora do escopo de busca.

Antes de gerar o código:
- explique brevemente as decisões técnicas;
- depois gere o código completo do search.py.