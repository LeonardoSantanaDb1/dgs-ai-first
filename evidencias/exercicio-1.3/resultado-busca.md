# Resultado da Busca Semântica

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04  

---

# Objetivo

Validar o funcionamento da etapa de recuperação semântica do pipeline RAG implementado para a NovaTech.

Os testes foram executados utilizando o script `search.py`, responsável por gerar embeddings da pergunta, consultar o ChromaDB e recuperar os chunks mais relevantes da base vetorial.

---

# Ambiente de Teste

## Modelo de Embeddings

```text
all-MiniLM-L6-v2
```

## Vector Store

```text
ChromaDB
```

## Collection

```text
novatech_docs
```

## Configuração

```text
Top-K = 3
```

---

# Teste 01

## Pergunta

```text
Qual o prazo de devolução para carga perigosa?
```

## Resultado Esperado

Recuperação prioritária da Política de Devolução POL-001, contendo a regra referente à exceção aplicada às cargas perigosas.

## Chunks Recuperados

| Ranking | Documento | Similaridade |
|----------|------------|------------|
| 1 | FAQ-atendimento.md | 0.6730 |
| 2 | POL-001-politica-devolucao.md | 0.6382 |
| 3 | PROC-042-frete-especial-v1.md | 0.6318 |

## Avaliação

Parcialmente correto.

Embora o mecanismo tenha recuperado documentos relacionados ao tema, a Política de Devolução não foi classificada em primeiro lugar.

O FAQ foi considerado mais relevante do que o documento normativo oficial.

## Observações

Foi identificado um possível problema de ranking semântico, onde documentos informais podem superar documentos normativos mesmo quando estes representam a fonte oficial da informação.

---

# Teste 02

## Pergunta

```text
Meu cliente é Gold, qual o SLA de resolução?
```

## Resultado Esperado

Recuperação prioritária do documento SLA-2024 contendo os tempos de resposta e resolução para clientes Gold.

## Chunks Recuperados

| Ranking | Documento | Similaridade |
|----------|------------|------------|
| 1 | FAQ-atendimento.md | 0.7011 |
| 2 | SLA-2024-tabela-sla-clientes.md | 0.5889 |
| 3 | FAQ-atendimento.md | 0.5620 |

## Avaliação

Parcialmente correto.

A resposta correta está presente no primeiro chunk recuperado.

Entretanto, novamente o FAQ foi priorizado em relação ao documento oficial.

## Observações

O comportamento reforça a hipótese de que o pipeline atualmente não diferencia autoridade documental durante a recuperação.

---

# Teste 03

## Pergunta

```text
Quanto custa o frete para 600kg para Manaus?
```

## Resultado Esperado

Recuperação do procedimento PROC-042-v2 contendo a fórmula de cálculo do frete especial.

## Chunks Recuperados

| Ranking | Documento | Similaridade |
|----------|------------|------------|
| 1 | PROC-042-frete-especial-v1.md | 0.5340 |
| 2 | PROC-042-v2-frete-especial-revisado.md | 0.5260 |
| 3 | PROC-042-v2-frete-especial-revisado.md | 0.5258 |

## Avaliação

Parcialmente correto.

O mecanismo recuperou os documentos corretos relacionados ao frete especial.

Entretanto, a versão antiga do procedimento foi classificada acima da versão revisada.

## Observações

Foi identificado um problema relacionado à coexistência de múltiplas versões do mesmo procedimento na base vetorial.

Sem metadados de vigência, o mecanismo não consegue distinguir automaticamente qual versão deve ser priorizada.

---

# Análise Geral dos Resultados

Os três testes demonstraram que o pipeline é funcional e capaz de recuperar documentos semanticamente relacionados às perguntas realizadas.

Os resultados indicam que:

- A ingestão foi realizada corretamente.
- Os embeddings foram gerados corretamente.
- A recuperação vetorial está funcionando.
- Os documentos relevantes estão sendo encontrados.

Entretanto, também foram observadas limitações importantes relacionadas à ordenação dos resultados.

---

# Problemas Identificados

## Problema 01 - FAQ Superando Documentos Oficiais

Em dois testes distintos, conteúdos provenientes do FAQ foram classificados acima de documentos normativos oficiais.

Esse comportamento pode levar à utilização de informações menos confiáveis durante a geração da resposta.

---

## Problema 02 - Ausência de Controle de Versão Documental

Os documentos PROC-042-v1 e PROC-042-v2 coexistem na mesma base vetorial.

Como não existem metadados de vigência, o mecanismo não possui capacidade de determinar automaticamente qual versão representa a regra atualmente válida.

---

# Melhorias Propostas

## Melhoria 01

Adicionar metadados de autoridade documental durante a ingestão.

Exemplo:

```text
POLÍTICA > PROCEDIMENTO > SLA > FAQ
```

Esses metadados poderiam ser utilizados para reordenar os resultados após a recuperação vetorial.

---

## Melhoria 02

Adicionar metadados de vigência documental.

Exemplo:

```text
versao=2
vigente=true
```

Dessa forma documentos obsoletos poderiam ser descartados ou priorizados adequadamente.

---

## Melhoria 03

Implementar etapa de re-ranking.

A utilização de um re-ranker permitiria refinar os resultados recuperados inicialmente pelo ChromaDB e aumentar a precisão das respostas.

---

# Conclusão

O pipeline de recuperação semântica demonstrou funcionamento adequado para uma prova de conceito.

Os documentos corretos foram recuperados em todos os testes realizados, comprovando a eficácia da estratégia de ingestão, geração de embeddings e armazenamento vetorial.

Entretanto, foram identificadas oportunidades de melhoria relacionadas à autoridade documental e ao tratamento de múltiplas versões de documentos.

Esses pontos não comprometem a validação da POC, mas representam evoluções recomendadas para uma implementação em ambiente produtivo.