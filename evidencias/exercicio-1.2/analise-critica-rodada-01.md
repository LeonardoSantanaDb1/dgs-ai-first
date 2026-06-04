# Análise Crítica das Respostas V1

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04

---

## Objetivo

Avaliar criticamente o comportamento do System Prompt V1 a partir das respostas geradas durante a primeira rodada de testes, verificando sua aderência aos guardrails definidos pelo negócio, à documentação fornecida e aos princípios de engenharia de contexto adotados para a solução.

---

## Avaliação Geral

Os resultados da primeira rodada de testes demonstram que o System Prompt V1 foi capaz de direcionar adequadamente o comportamento do assistente, reduzindo riscos de alucinação e promovendo respostas fundamentadas na documentação disponível.

As três respostas respeitaram os guardrails definidos para o projeto e apresentaram evidências de utilização correta dos chunks fornecidos.

De forma geral, o assistente demonstrou capacidade de:

- Utilizar exclusivamente as informações presentes nos documentos recuperados.
- Citar explicitamente as fontes utilizadas.
- Respeitar exceções documentais.
- Evitar inferências não suportadas pela documentação.
- Reconhecer situações em que não existiam informações suficientes para responder.

---

## Critérios Avaliados

Durante a análise das respostas foram considerados os seguintes critérios:

- Aderência aos guardrails definidos pelo negócio.
- Utilização exclusiva das informações presentes nos chunks recuperados.
- Capacidade de identificar exceções documentais.
- Correção das informações apresentadas.
- Citação explícita das fontes utilizadas.
- Tratamento adequado de cenários com informações insuficientes.
- Ausência de alucinações ou inferências não suportadas pela documentação.

Esses critérios foram utilizados como base para determinar se o comportamento do assistente estava alinhado aos requisitos definidos para a solução.

---

## Pergunta 01 - Carga Perigosa

### Pergunta

Qual o prazo de devolução para carga perigosa?

### Resultado

Correto.

### Evidências

O assistente identificou corretamente que a exceção documental possui prioridade sobre a regra geral de devolução.

A resposta não reproduziu incorretamente o prazo de 7 dias úteis e destacou a ausência de procedimento alternativo na documentação disponível.

Também foi observado que o assistente recomendou escalonamento para o supervisor diante da ausência de informações complementares, comportamento alinhado aos guardrails definidos para o projeto.

### Avaliação

O comportamento está alinhado com os requisitos do projeto.

Este teste era considerado um dos principais cenários de validação, pois avaliava a capacidade do modelo de reconhecer exceções documentais e evitar respostas baseadas apenas na regra geral.

---

## Pergunta 02 - SLA Cliente Gold

### Pergunta

Meu cliente é Gold, qual o SLA de resolução?

### Resultado

Correto.

### Evidências

O assistente recuperou corretamente a informação da tabela SLA-2024 e apresentou a resposta de forma objetiva.

A fonte foi citada corretamente e não foram adicionadas informações inexistentes na documentação.

### Avaliação

A resposta está adequada e não foram identificados problemas relevantes.

O comportamento demonstra aderência aos princípios de grounding e recuperação correta de informações estruturadas.

---

## Pergunta 03 - Frete para Manaus

### Pergunta

Quanto custa o frete para 600kg para Manaus?

### Resultado

Correto.

### Evidências

O assistente identificou corretamente que não existem informações suficientes para calcular o valor final do frete.

A resposta não inventou valores, não realizou cálculos indevidos e explicou claramente quais informações estavam ausentes para concluir a solicitação.

Também foi observado que o assistente evitou utilizar conhecimento externo para associar a cidade de Manaus a uma determinada região geográfica, limitando-se exclusivamente às informações presentes na documentação disponível.

### Avaliação

O comportamento está alinhado com os guardrails definidos.

A resposta demonstra um controle adequado sobre alucinações e evidencia que o prompt conseguiu restringir o uso de conhecimento não documentado.

Entretanto, observou-se uma oportunidade de melhoria relacionada à explicitação da proibição do uso de conhecimento externo durante a interpretação de localidades, regiões ou informações não presentes nos documentos recuperados.

---

## Pontos Fortes Identificados

Os principais pontos positivos observados durante os testes foram:

- Correta identificação de exceções documentais.
- Respostas fundamentadas na documentação recuperada.
- Citação consistente das fontes utilizadas.
- Ausência de alucinações.
- Tratamento adequado de cenários com informações insuficientes.
- Respeito aos guardrails definidos para o negócio.
- Linguagem formal e acessível.

---

## Oportunidades de Melhoria

Embora o comportamento geral tenha sido satisfatório, foram identificadas oportunidades para fortalecer o prompt:

- Reforçar explicitamente a proibição do uso de conhecimento externo.
- Reforçar a distinção entre conhecimento documental e conhecimento pré-treinado.
- Tornar mais explícita a necessidade de justificar respostas incompletas quando houver ausência de informações suficientes.
- Padronizar a forma de comunicação quando não houver evidências suficientes para responder uma consulta.

Nenhuma das oportunidades identificadas representa falha crítica da solução, mas sua incorporação tende a aumentar a robustez do comportamento do assistente em cenários mais complexos.

---

## Ajustes Planejados para a Versão V2

Com base nos resultados observados, os seguintes ajustes serão incorporados na próxima versão do prompt:

- Reforço explícito da proibição de utilização de conhecimento externo ao contexto recuperado.
- Reforço da distinção entre conhecimento documental e conhecimento pré-treinado do modelo.
- Padronização da justificativa apresentada quando informações necessárias não estiverem disponíveis na documentação.
- Maior detalhamento das instruções relacionadas ao tratamento de informações incompletas.
- Reforço das instruções relacionadas ao grounding e à utilização exclusiva das fontes documentais.

Esses ajustes possuem caráter preventivo e visam aumentar a robustez da solução para cenários mais complexos do que os avaliados nesta primeira rodada.

---

## Conclusão

O System Prompt V1 apresentou comportamento adequado para os cenários avaliados e demonstrou aderência aos guardrails definidos para o projeto.

Os resultados obtidos indicam que a estratégia de engenharia de contexto adotada foi eficaz para direcionar o comportamento do assistente, reduzindo riscos de alucinação e aumentando a confiabilidade das respostas.

As melhorias propostas possuem caráter evolutivo e serão incorporadas à versão V2 do prompt com o objetivo de aumentar a robustez da solução e melhorar sua capacidade de lidar com cenários de documentação incompleta, ambígua ou conflitante.