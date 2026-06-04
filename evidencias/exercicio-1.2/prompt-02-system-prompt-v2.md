# Prompt 02 - System Prompt V2

**Nome:** Leonardo Santana
**Papel/Cargo:** Desenvolvedor
**Data:** 2026-06-04

---

## Objetivo

Construir uma segunda versão do System Prompt do assistente corporativo da NovaTech, incorporando os ajustes identificados durante a análise crítica da primeira rodada de testes.

O objetivo desta iteração é aumentar a robustez do comportamento do assistente, reforçando os mecanismos de grounding, reduzindo riscos relacionados ao uso de conhecimento externo e melhorando o tratamento de cenários onde a documentação disponível não contém informações suficientes para responder uma consulta.

---

## Motivação da Iteração

A primeira rodada de testes apresentou resultados satisfatórios e demonstrou aderência aos guardrails definidos para o projeto.

Entretanto, foram identificadas oportunidades de melhoria relacionadas aos seguintes aspectos:

- Reforço explícito da proibição do uso de conhecimento externo.
- Maior distinção entre conhecimento documental e conhecimento pré-treinado do modelo.
- Padronização do comportamento quando informações necessárias não estiverem presentes na documentação.
- Reforço das instruções relacionadas ao grounding e à utilização exclusiva dos documentos recuperados.

Esses ajustes possuem caráter preventivo e visam aumentar a confiabilidade da solução em cenários mais complexos.

---

## Referência

O conteúdo completo do System Prompt V2 encontra-se documentado em:

```text
.spec/exercicio-1.2-prototipacao-system-prompt.md
```

---

## Principais Ajustes Incorporados

- Reforço da utilização exclusiva das informações presentes nos documentos recuperados.
- Proibição explícita da utilização de conhecimento externo para complementar respostas.
- Maior detalhamento do comportamento esperado quando informações estiverem ausentes.
- Reforço dos mecanismos de grounding.
- Padronização das respostas para cenários de informação insuficiente.

---

## Utilização

A versão V2 do System Prompt foi utilizada durante a segunda rodada de testes do exercício, empregando os mesmos chunks documentais e os mesmos cenários utilizados na primeira rodada, permitindo comparação direta entre os resultados obtidos.