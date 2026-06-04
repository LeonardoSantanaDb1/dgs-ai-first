# Teste End-to-End

**Nome:** Leonardo Santana
**Papel/Cargo:** Desenvolvedor
**Data:** 2026-06-04

---

# Pergunta

Qual o prazo de devolução para carga perigosa?

---

# Objetivo

Validar o funcionamento completo do pipeline RAG, desde a recuperação semântica até a geração da resposta pelo modelo de linguagem.

---

# Fluxo Executado

Pergunta
↓
search.py
↓
ChromaDB
↓
Chunks Recuperados
↓
prompt_builder.py
↓
Claude
↓
Resposta

---

# Chunks Recuperados

## Chunk 01

Fonte:

```text
FAQ-atendimento.md
```

Conteúdo relacionado ao tratamento especial de cargas perigosas.

---

## Chunk 02

Fonte:

```text
POL-001-politica-devolucao.md
```

Conteúdo relacionado aos custos e condições gerais de devolução.

---

## Chunk 03

Fonte:

```text
PROC-042-frete-especial-v1.md
```

Conteúdo relacionado ao prazo de entrega para frete especial.

---

# Resposta Gerada pelo Claude

Resposta:

Não foi localizado, no contexto fornecido, um prazo de devolução específico para carga perigosa.

As informações disponíveis indicam que a devolução de carga perigosa não segue o processo padrão e deve ser tratada como exceção, por meio de contato com a Gestão de Riscos.

Como não há informação suficiente para confirmar um prazo, recomenda-se escalar a questão ao supervisor.

Fonte:

FAQ-atendimento.md (chunk 2)

POL-001-politica-devolucao.md (chunk 8)

Observações:

- A devolução de carga perigosa exige tratamento especial.
- O prazo de 7 dias úteis refere-se apenas ao processo padrão.
- O documento PROC-042 não é aplicável à pergunta.

---

# Avaliação

## Recuperação

Parcialmente correta.

O mecanismo recuperou documentos relacionados ao tema da pergunta.

Entretanto, o chunk normativo ideal não foi recuperado.

---

## Resposta

Correta dentro do contexto disponível.

O Claude respeitou integralmente os guardrails definidos.

Não foram observadas alucinações.

O modelo não inventou prazos nem utilizou conhecimento externo.

---

## Fontes

As fontes utilizadas foram corretamente citadas.

---

## Grounding

A resposta permaneceu integralmente fundamentada nos documentos recuperados.

---

# Conclusão

O teste validou com sucesso o funcionamento ponta a ponta do pipeline RAG.

Foi possível comprovar a integração entre ingestão, recuperação vetorial, montagem de contexto e geração de resposta.

Também foi identificado um problema real relacionado à qualidade da recuperação semântica, evidenciando uma oportunidade concreta de evolução para futuras versões da solução.