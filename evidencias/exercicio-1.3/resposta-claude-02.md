# Resposta Claude 02 - Implementação da Ingestão do Pipeline RAG

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04  

--- 

# Objetivo da Interação

Solicitar apoio do Claude Code para implementação da etapa de ingestão do pipeline RAG da NovaTech, utilizando ferramentas gratuitas e open-source.

O objetivo era obter uma implementação funcional capaz de:

- Ler documentos Markdown.
- Aplicar chunking.
- Gerar embeddings.
- Persistir vetores no ChromaDB.
- Armazenar metadados para rastreabilidade.

---

# Resposta Gerada pelo Claude

## Análise da Arquitetura

O Claude realizou uma avaliação prévia da arquitetura proposta antes de gerar a implementação.

### Estratégia de Chunking

Foi sugerida a utilização de chunking baseado em estrutura semântica dos documentos, aproveitando os títulos e subtítulos existentes nos arquivos Markdown.

Segundo a análise, essa abordagem reduz o risco de fragmentação inadequada das informações e preserva melhor o significado dos documentos durante a recuperação.

Também foi sugerida a utilização de overlap para seções maiores, reduzindo perdas de contexto em limites de segmentação.

---

### Modelo de Embeddings

O modelo all-MiniLM-L6-v2 foi considerado adequado para a prova de conceito por apresentar:

- Baixo consumo de recursos.
- Execução local.
- Boa velocidade de processamento.
- Compatibilidade com português.

Foi destacado que modelos multilíngues poderiam apresentar melhor desempenho em cenários produtivos.

---

### Banco Vetorial

A utilização do ChromaDB local foi considerada adequada para o escopo da prova de conceito.

A estrutura já definida para armazenamento dos vetores foi validada.

---

# Riscos Identificados

## LangChain

### Problema

O arquivo requirements.txt continha dependência do LangChain.

### Impacto

O exercício não exige LangChain e a sua utilização aumentaria a complexidade da solução sem necessidade.

### Ação Proposta

Remoção da dependência.

---

## Conflito Entre Versões Documentais

### Problema

Os documentos:

- PROC-042-v1
- PROC-042-v2

serão indexados simultaneamente.

### Impacto

Consultas futuras podem recuperar versões diferentes do mesmo procedimento.

### Risco

O pipeline poderá retornar informações conflitantes caso não exista mecanismo de controle de vigência documental.

---

## FAQ Misturado com Documentação Normativa

### Problema

O FAQ será indexado juntamente com documentos oficiais.

### Impacto

Informações informais podem competir com procedimentos normativos durante a recuperação.

### Risco

Respostas menos confiáveis ou inconsistentes.

---

## Estrutura de Tabelas

### Problema

Tabelas Markdown podem perder parte de sua estrutura semântica durante a vetorização.

### Impacto

Possível redução da qualidade da recuperação para consultas relacionadas a multiplicadores de frete e regras tabulares.

---

# Implementação Gerada

O Claude gerou a implementação completa do arquivo:

```text
src/ingest.py
```

Responsabilidades implementadas:

- Leitura automática dos documentos da pasta docs.
- Aplicação de chunking baseado em seções semânticas.
- Subdivisão de seções extensas utilizando overlap.
- Geração de embeddings através do modelo all-MiniLM-L6-v2.
- Criação da coleção vetorial no ChromaDB.
- Persistência dos vetores.
- Armazenamento de metadados.
- Reprocessamento completo da coleção a cada execução.

---

# Ajustes Realizados Pelo Claude

Além da implementação do ingest.py, o Claude realizou a seguinte correção:

### Arquivo

```text
requirements.txt
```

### Alteração

Remoção da dependência:

```text
langchain
```

### Justificativa

A biblioteca não é necessária para o escopo da prova de conceito e não faz parte dos requisitos obrigatórios do exercício.

---

# Decisões Técnicas Adotadas

## Chunking Semântico

O chunking foi baseado na estrutura lógica dos documentos.

Motivação:

- Preservação de contexto.
- Menor fragmentação.
- Melhor recuperação semântica.

---

## Overlap

Foi adotada sobreposição entre chunks para reduzir perda de contexto.

Motivação:

- Melhor recuperação de informações localizadas próximas aos limites de segmentação.

---

## Similaridade Cosseno

Foi utilizada similaridade baseada em cosseno.

Motivação:

- Melhor comparação semântica entre embeddings.
- Menor influência do tamanho dos documentos.

---

## Reprocessamento Completo

A coleção vetorial é recriada a cada execução.

Motivação:

- Simplificar o fluxo da prova de conceito.
- Evitar duplicação de documentos durante os testes.

---

# Resultado da Interação

A interação produziu uma implementação funcional da etapa de ingestão do pipeline RAG e identificou riscos importantes relacionados à governança documental, recuperação semântica e qualidade dos dados indexados.

As observações apresentadas serão avaliadas criticamente antes da incorporação definitiva na arquitetura da solução.

---

# Próximos Passos

- Revisar criticamente as recomendações apresentadas.
- Validar a implementação do ingest.py.
- Executar a indexação dos documentos.
- Implementar a etapa de busca semântica.
- Construir a montagem de prompt.
- Realizar os testes exigidos pelo exercício.