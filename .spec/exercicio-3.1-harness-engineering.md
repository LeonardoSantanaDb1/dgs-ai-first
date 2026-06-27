# Exercício 3.1 — Structured Output e Verificações Determinísticas (Harness Engineering)

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-27

---

# Análise Inicial (Humana)

## Entendimento do Problema

O assistente da NovaTech já possui um pipeline RAG funcional, porém as respostas ainda são retornadas em formato de texto livre.

Nesse cenário não existe garantia determinística de que informações obrigatórias, como o documento fonte e o nível de confiança, estejam sempre presentes ou sejam consistentes.

Além disso, determinadas regras de negócio críticas dependem apenas do comportamento probabilístico do modelo, aumentando o risco de respostas incorretas chegarem ao usuário.

O objetivo deste exercício é fortalecer o harness da aplicação através da combinação de Structured Outputs com validações determinísticas implementadas em código.

---

## Premissas Identificadas

- O modelo continuará sendo probabilístico.
- O código será responsável pelas validações determinísticas.
- Toda resposta deverá possuir um documento fonte.
- Regras críticas de negócio devem ser protegidas por guardrails.
- O validator deve bloquear respostas inválidas antes que sejam entregues ao usuário.

---

## Requisitos Identificados

A partir da análise do enunciado foram identificados os seguintes requisitos técnicos:

- utilização de Structured Outputs;
- validação através de Zod;
- implementação de dois guardrails determinísticos;
- utilização de logging estruturado;
- retorno de uma resposta segura em qualquer falha de validação.

---

## Estratégia Inicial

A solução será composta por um módulo responsável por:

1. validar estruturalmente a resposta do modelo utilizando Zod;
2. aplicar os guardrails determinísticos;
3. registrar os motivos de rejeição;
4. substituir respostas inválidas por uma resposta segura.

Essa abordagem garante que regras críticas de negócio não dependam exclusivamente do comportamento probabilístico do modelo.

---

# Solução Inicial (Claude)

Foi elaborado um prompt descrevendo o contexto do projeto, os requisitos técnicos, os guardrails obrigatórios e as restrições de implementação.

A implementação inicial gerada pelo Claude contemplou:

- schema Zod;
- validação estrutural;
- implementação dos dois guardrails;
- resposta segura de fallback;
- logging com Pino.

Essa implementação foi utilizada como ponto de partida para a revisão técnica.

---

# Revisão Técnica

## Análise Humana

Antes da etapa de refinamento foi realizada uma revisão técnica da implementação inicial.

Foram identificadas oportunidades de melhoria relacionadas principalmente a:

- endurecimento do Schema Zod;
- robustez do Guardrail de carga perigosa;
- exposição excessiva de informações em logs;
- imutabilidade da resposta segura;
- validação de campos contendo apenas espaços em branco.

---

## Code Review do Claude

A implementação também foi submetida a uma revisão técnica utilizando o Claude.

As principais observações complementares foram:

- utilização de `.strict()` no Schema Zod;
- fortalecimento do Guardrail utilizando expressões regulares;
- utilização de `Object.freeze()` na resposta de fallback;
- melhoria na estratégia de logging;
- extração da normalização textual para função reutilizável.

---

## Consolidação das Decisões

Após comparar a revisão humana com a revisão realizada pelo Claude, foram aprovadas apenas as melhorias aderentes ao objetivo do exercício.

Melhorias implementadas:

- Schema Zod utilizando `.strict()`;
- validação de campos contendo apenas espaços;
- reforço do Guardrail 2 utilizando RegExp;
- redução da exposição de informações em logs;
- resposta de fallback imutável.

Melhorias registradas para evolução futura:

- allowlist de documentos válidos;
- threshold para `confidence_score`;
- ajustes na estratégia de observabilidade.

---

# Solução Refinada

A implementação final do `response-validator.ts` passou a oferecer:

- validação estrutural determinística através de Zod;
- contrato rígido do Structured Output;
- validação de conteúdo obrigatório;
- dois guardrails determinísticos;
- resposta segura para qualquer falha;
- logging estruturado;
- maior robustez contra respostas inconsistentes.

A arquitetura original foi preservada, incorporando apenas as melhorias aprovadas durante a revisão técnica.

---

# Diferença entre Prompt e Código

Durante a implementação foi possível observar claramente a diferença entre validações probabilísticas e determinísticas.

O prompt orienta o comportamento esperado do modelo, porém não garante seu cumprimento.

Já o código executa validações determinísticas capazes de rejeitar qualquer resposta que viole o contrato estabelecido.

Essa combinação fortalece o Harness Engineering ao reduzir a dependência exclusiva do comportamento do modelo.

---

# Evidências Produzidas

Durante o desenvolvimento foram produzidos os seguintes artefatos:

- Prompt inicial;
- Resposta inicial do Claude;
- Análise técnica do desenvolvedor;
- Prompt para Code Review;
- Code Review do Claude;
- Consolidação das decisões técnicas;
- Prompt de refinamento;
- Implementação final do `response-validator.ts`.

---

# Conclusão

O Exercício 3.1 demonstrou como Structured Outputs e validações determinísticas podem ser utilizados para aumentar a confiabilidade de aplicações baseadas em IA Generativa.

A utilização do Claude ocorreu como apoio ao desenvolvimento, enquanto as decisões técnicas permaneceram sob responsabilidade do desenvolvedor.

O resultado final atende aos requisitos do exercício ao combinar validação estrutural, guardrails determinísticos e resposta segura, reduzindo riscos associados ao comportamento probabilístico do modelo.