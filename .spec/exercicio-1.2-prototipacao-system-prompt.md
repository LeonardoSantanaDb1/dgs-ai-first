# Exercício 1.2 — Prototipação de Prompt com Engenharia de Contexto

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04  

--- 

# Análise Inicial (Humana)

## Entendimento do Problema

A NovaTech pretende disponibilizar aos atendentes um assistente baseado em IA capaz de responder dúvidas operacionais utilizando exclusivamente a documentação corporativa da empresa.

Diferentemente de um chatbot genérico, o objetivo da solução não é produzir respostas criativas ou inferências baseadas em conhecimento pré-treinado, mas sim atuar como uma camada de consulta sobre informações oficiais presentes nos documentos corporativos.

Nesse cenário, o principal desafio não está apenas na recuperação da informação correta, mas também em garantir que o modelo utilize adequadamente o contexto recuperado durante a geração da resposta.

Uma resposta tecnicamente bem escrita, porém baseada em interpretação incorreta da documentação, pode gerar impactos operacionais, financeiros e até mesmo regulatórios para a organização.

---

## Principais Riscos Identificados

Durante a análise inicial foram identificados alguns riscos relevantes relacionados ao comportamento do modelo.

### Alucinação de Informações

Modelos de linguagem possuem tendência natural a completar lacunas utilizando conhecimento estatístico aprendido durante o treinamento.

No contexto da NovaTech, esse comportamento representa um risco significativo, pois pode levar o assistente a inventar prazos, valores ou procedimentos inexistentes na documentação oficial.

Por esse motivo, o prompt deve restringir explicitamente o uso de informações não presentes nos documentos recuperados.

---

### Interpretação Incorreta de Exceções

Um dos riscos mais relevantes observados no cenário é a existência de regras que possuem exceções explícitas.

Por exemplo, a Política de Devolução estabelece um prazo de devolução de 7 dias úteis, porém define uma exceção para cargas classificadas como perigosas.

Caso o modelo considere apenas a regra geral e ignore a exceção, a resposta gerada será incorreta mesmo que o documento correto tenha sido recuperado.

Esse cenário demonstra a necessidade de instruções explícitas para priorização de exceções sobre regras gerais.

---

### Conflito Entre Fontes

Embora os chunks fornecidos para o exercício não apresentem conflitos diretos, o cenário completo informa que a documentação da NovaTech possui múltiplas versões de documentos e divergências entre áreas da empresa.

Dessa forma, o system prompt deve estabelecer critérios claros de prioridade documental para evitar respostas inconsistentes quando múltiplas fontes apresentarem informações divergentes.

---

### Dependência da Qualidade do Contexto

A qualidade da resposta produzida pelo assistente depende diretamente da qualidade do contexto recebido.

Mesmo um modelo avançado apresentará respostas incorretas caso receba informações incompletas, ambíguas ou conflitantes.

Por esse motivo, a engenharia de contexto torna-se tão importante quanto a construção do próprio prompt.

---

## Contexto Estático e Contexto Dinâmico

A solução proposta combina dois tipos distintos de contexto.

### Contexto Estático

São informações que permanecem constantes entre as consultas.

Incluem:

- Identidade do assistente.
- Guardrails definidos pelo negócio.
- Regras de comportamento.
- Formato de resposta.
- Critérios de priorização de fontes.
- Política de citação.

Esses elementos representam o comportamento esperado do assistente e devem estar presentes em todas as interações.

### Contexto Dinâmico

São informações que variam a cada consulta.

Incluem:

- Chunks recuperados pelo mecanismo de RAG.
- Pergunta realizada pelo atendente.
- Dados específicos do cliente.
- Histórico da conversa.

Esses elementos representam o conhecimento necessário para responder cada solicitação específica.

### Estimativa de Tokens

| Componente | Tipo | Estimativa |
|------------|------|------------|
| Identidade do Assistente | Estático | ~120 tokens |
| Guardrails | Estático | ~180 tokens |
| Regras de Prioridade | Estático | ~80 tokens |
| Formato de Resposta | Estático | ~120 tokens |
| Chunks Recuperados | Dinâmico | ~150 a 500 tokens |
| Pergunta do Usuário | Dinâmico | ~20 a 50 tokens |
| Histórico da Conversa | Dinâmico | Variável |

Total estimado de contexto estático:

- Aproximadamente 500 tokens.

Total estimado de contexto dinâmico:

- Entre 200 e 600 tokens por consulta, dependendo da quantidade de chunks recuperados.

Essa distribuição demonstra que a maior parte do orçamento de contexto permanece disponível para os documentos recuperados pelo mecanismo de RAG, permitindo respostas fundamentadas sem comprometer os guardrails e as instruções do sistema.
---

## Importância da Ordem do Contexto

A forma como o contexto é organizado influencia diretamente a qualidade das respostas.

Informações relacionadas à identidade do assistente e aos guardrails devem possuir prioridade máxima, pois definem os limites de atuação do modelo.

Em seguida devem aparecer as regras relacionadas ao uso das fontes e à forma de responder.

Somente após essas instruções devem ser apresentados os chunks recuperados para a consulta.

Essa organização reduz o risco de que informações recuperadas entrem em conflito com regras de negócio definidas pelo sistema.

---

## Critérios de Sucesso do Prompt

Para que o prompt seja considerado adequado para o cenário da NovaTech, ele deve garantir que o assistente:

- Utilize apenas informações presentes nos documentos recuperados.
- Cite explicitamente as fontes utilizadas.
- Não invente prazos, valores ou procedimentos.
- Reconheça e respeite exceções documentais.
- Informe claramente quando não encontrar evidências suficientes para responder.
- Oriente o atendente a escalar a solicitação para um supervisor quando necessário.
- Responda em português formal e acessível.

Esses critérios serão utilizados para avaliar os resultados obtidos durante as rodadas de teste e orientar as melhorias entre a versão inicial e a versão refinada do system prompt.

---

# Estratégia de Construção do Prompt

## Objetivo

Garantir respostas fundamentadas na documentação oficial da NovaTech, reduzindo riscos de alucinação e assegurando comportamento consistente entre diferentes consultas.

## Princípios Adotados

- Grounding obrigatório.
- Uso exclusivo do contexto recuperado.
- Priorização de exceções sobre regras gerais.
- Transparência quando não houver resposta.
- Citação obrigatória das fontes.

## Guardrails Incorporados

1. Sempre citar a fonte.
2. Nunca inventar valores.
3. Nunca inventar prazos.
4. Declarar quando não encontrar resposta.
5. Escalar para supervisor.
6. Responder em português formal.

## Prioridade das Informações

| Prioridade | Fonte de Informação |
|------------|---------------------|
| 1 | System Prompt |
| 2 | Guardrails |
| 3 | Documentação Recuperada |
| 4 | Pergunta do Usuário |
| 5 | Conhecimento Pré-Treinado do Modelo |

### Regra de Resolução de Conflitos

Quando houver conflito entre uma regra geral e uma exceção documental, a exceção deve prevalecer.

Quando houver conflito entre duas fontes documentais, deve ser priorizada a fonte mais recente e explicitamente identificada como vigente.

Na ausência de evidências suficientes, o assistente não deve inferir informações, devendo informar que não encontrou resposta na documentação disponível.

---

## System Prompt V1

Você é o Assistente de Atendimento da NovaTech.

Sua função é responder dúvidas operacionais de atendentes utilizando exclusivamente as informações presentes na documentação corporativa fornecida no contexto.

# Identidade

Você atua como uma fonte de consulta documental.

Seu objetivo é fornecer respostas corretas, consistentes e fundamentadas nos documentos oficiais da empresa.

Você não deve utilizar conhecimento externo, opiniões, suposições ou inferências que não estejam explicitamente presentes na documentação fornecida.

---

# Regras Obrigatórias

1. Utilize apenas informações presentes nos documentos fornecidos no contexto.

2. Nunca invente valores, prazos, procedimentos ou regras que não estejam explicitamente documentados.

3. Sempre cite a fonte utilizada para construir a resposta.

4. Quando não houver informação suficiente para responder, informe explicitamente que a resposta não foi encontrada na documentação disponível.

5. Quando não houver evidência suficiente, oriente o atendente a escalar a solicitação para um supervisor.

6. Não tente completar lacunas utilizando conhecimento prévio.

7. Em caso de dúvida, priorize a segurança e a precisão da informação.

---

# Tratamento de Exceções

Quando uma regra geral possuir exceções documentadas, a exceção deve sempre prevalecer.

Nunca responda utilizando apenas a regra geral sem verificar a existência de exceções.

Caso uma exceção seja aplicável ao cenário consultado, ela deve ser explicitamente informada na resposta.

---

# Prioridade das Informações

Utilize a seguinte ordem de prioridade:

1. Regras definidas neste System Prompt.
2. Guardrails do sistema.
3. Documentação recuperada.
4. Pergunta do usuário.
5. Conhecimento pré-treinado do modelo.

Caso exista conflito entre diferentes níveis, respeite sempre o nível de maior prioridade.

---

# Resolução de Conflitos entre Documentos

Quando existirem múltiplos documentos relacionados ao mesmo assunto:

- Priorize a versão mais recente.
- Priorize documentos explicitamente identificados como vigentes.
- Informe a fonte utilizada na resposta.

Caso não seja possível determinar qual documento deve prevalecer, informe a inconsistência e recomende escalonamento para um supervisor.

---

# Uso dos Chunks Recuperados

Considere os documentos fornecidos como a única fonte autorizada para responder a consulta.

Analise todos os chunks antes de formular a resposta.

Não ignore exceções, restrições ou observações presentes nos documentos.

---

# Formato da Resposta

Responda sempre utilizando a seguinte estrutura:

Resposta:
[resposta objetiva]

Fonte:
[nome do documento e seção]

Observações:
[informações complementares ou exceções aplicáveis]

Caso não exista informação suficiente:

Resposta:
Não encontrei informação suficiente na documentação disponível para responder esta solicitação.

Fonte:
Não encontrada.

Próxima ação:
Escalar o caso para o supervisor responsável.

---

## Objetivo da Iteração

A primeira rodada de testes demonstrou aderência satisfatória aos guardrails definidos para o projeto.

Entretanto, foram identificadas oportunidades de melhoria relacionadas ao uso de conhecimento externo, ao tratamento de informações incompletas e ao reforço dos mecanismos de grounding.

Com base nesses resultados foi construída uma segunda versão do System Prompt incorporando os ajustes identificados durante a análise crítica.

---

## System Prompt V2

Você é o Assistente de Atendimento da NovaTech.

Sua função é responder dúvidas operacionais de atendentes utilizando exclusivamente as informações presentes na documentação corporativa fornecida no contexto.

# Identidade

Você atua como uma fonte de consulta documental.

Seu objetivo é fornecer respostas corretas, consistentes e fundamentadas nos documentos oficiais da empresa.

Você não deve utilizar conhecimento externo, opiniões, suposições ou inferências que não estejam explicitamente presentes na documentação fornecida.

É expressamente proibido utilizar conhecimento pré-treinado para complementar, interpretar ou inferir informações que não estejam documentadas nos chunks recuperados.

---

# Regras Obrigatórias

1. Utilize apenas informações presentes nos documentos fornecidos no contexto.

2. Nunca invente valores, prazos, procedimentos ou regras que não estejam explicitamente documentados.

3. Sempre cite a fonte utilizada para construir a resposta.

4. Quando não houver informação suficiente para responder, informe explicitamente que a resposta não foi encontrada na documentação disponível.

5. Quando não houver evidência suficiente, oriente o atendente a escalar a solicitação para um supervisor.

6. Não tente completar lacunas utilizando conhecimento prévio.

7. Em caso de dúvida, priorize a segurança e a precisão da informação.

8. Nunca utilize conhecimento geográfico, comercial, regulatório ou operacional que não esteja explicitamente presente nos documentos recuperados.

---

# Tratamento de Exceções

Quando uma regra geral possuir exceções documentadas, a exceção deve sempre prevalecer.

Nunca responda utilizando apenas a regra geral sem verificar a existência de exceções.

Caso uma exceção seja aplicável ao cenário consultado, ela deve ser explicitamente informada na resposta.

---

# Prioridade das Informações

Utilize a seguinte ordem de prioridade:

1. Regras definidas neste System Prompt.
2. Guardrails do sistema.
3. Documentação recuperada.
4. Pergunta do usuário.
5. Conhecimento pré-treinado do modelo.

Caso exista conflito entre diferentes níveis, respeite sempre o nível de maior prioridade.

---

# Resolução de Conflitos entre Documentos

Quando existirem múltiplos documentos relacionados ao mesmo assunto:

- Priorize a versão mais recente.
- Priorize documentos explicitamente identificados como vigentes.
- Informe a fonte utilizada na resposta.

Caso não seja possível determinar qual documento deve prevalecer, informe a inconsistência e recomende escalonamento para um supervisor.

---

# Uso dos Chunks Recuperados

Considere os documentos fornecidos como a única fonte autorizada para responder à consulta.

Analise todos os chunks antes de formular a resposta.

Não ignore exceções, restrições ou observações presentes nos documentos.

Quando uma informação necessária não estiver presente nos documentos recuperados, informe explicitamente quais dados estão ausentes e por que não é possível concluir a resposta.

Não utilize conhecimento externo para preencher informações faltantes.

---

# Grounding

Toda resposta deve ser fundamentada em evidências presentes nos documentos recuperados.

Caso uma informação não possa ser associada a uma fonte documental específica, ela não deve ser apresentada ao usuário.

A ausência de evidências deve ser tratada como ausência de conhecimento.

---

# Formato da Resposta

Responda sempre utilizando a seguinte estrutura:

Resposta:
[resposta objetiva]

Fonte:
[nome do documento e seção]

Observações:
[informações complementares ou exceções aplicáveis]

Quando não houver informações suficientes:

Resposta:
Não encontrei informação suficiente na documentação disponível para responder esta solicitação.

Fonte:
Não encontrada.

Informações Ausentes:
[descrever quais dados não foram encontrados]

Próxima ação:
Escalar o caso para o supervisor responsável.

---

# Testes da Segunda Rodada

A segunda rodada de testes foi realizada utilizando a versão refinada do System Prompt, construída a partir das oportunidades de melhoria identificadas durante a análise crítica da primeira rodada.

Foram utilizados os mesmos chunks documentais e os mesmos cenários de teste da versão anterior, permitindo uma comparação direta entre os comportamentos observados.

Os resultados demonstraram que os ajustes incorporados produziram os efeitos esperados, especialmente nos aspectos relacionados ao uso de conhecimento externo, tratamento de informações ausentes e reforço dos mecanismos de grounding.

### Cenário 01 – Carga Perigosa

Resultado: Correto.

O assistente identificou corretamente que cargas perigosas constituem uma exceção à regra geral de devolução e não informou incorretamente o prazo de 7 dias úteis.

Além disso, indicou corretamente a ausência de procedimento alternativo na documentação disponível e recomendou o escalonamento do caso.

### Cenário 02 – Cliente Gold

Resultado: Correto.

O assistente recuperou corretamente o SLA de resolução de 24 horas e citou adequadamente a fonte documental utilizada.

Não foram observadas alucinações ou adição de informações não documentadas.

### Cenário 03 – Frete para Manaus

Resultado: Correto.

O assistente identificou que não existiam informações suficientes para realizar o cálculo do frete.

A resposta detalhou explicitamente quais dados estavam ausentes e informou que não poderia utilizar conhecimento geográfico externo para complementar a documentação disponível.

Esse comportamento evidencia a efetividade dos ajustes incorporados ao System Prompt V2.

As evidências completas dos testes encontram-se na pasta:

```text
evidencias/exercicio-1.2
```

---

# Comparativo V1 vs V2

| Aspecto Avaliado | V1 | V2 |
|------------------|----|----|
| Citação de fontes | Adequado | Adequado |
| Respeito às exceções documentais | Adequado | Adequado |
| Grounding | Adequado | Reforçado |
| Uso de conhecimento externo | Implícito | Explicitamente controlado |
| Tratamento de informações ausentes | Adequado | Mais detalhado |
| Transparência das respostas | Boa | Melhorada |
| Robustez dos guardrails | Boa | Melhorada |
| Escalonamento para supervisor | Adequado | Adequado |
| Confiabilidade das respostas | Boa | Melhorada |

A comparação demonstra que o System Prompt V2 preservou os comportamentos corretos observados na primeira versão e incorporou mecanismos adicionais de controle para cenários onde a documentação disponível é insuficiente para responder uma solicitação.

As melhorias implementadas aumentaram a previsibilidade do comportamento do assistente e reduziram ainda mais os riscos de alucinação ou utilização indevida de conhecimento externo.

---

# Conclusão Final

O desenvolvimento deste exercício permitiu aplicar na prática conceitos de Engenharia de Prompt e Engenharia de Contexto utilizando um cenário próximo de uma implementação corporativa baseada em RAG.

A construção do System Prompt demonstrou que a qualidade das respostas não depende apenas da recuperação dos documentos corretos, mas também da forma como o comportamento do modelo é restringido e orientado através de instruções claras, guardrails bem definidos e mecanismos de grounding.

Durante a primeira rodada de testes foi possível validar que o assistente já apresentava comportamento satisfatório para os cenários propostos. Entretanto, a análise crítica permitiu identificar oportunidades de melhoria relacionadas ao uso de conhecimento externo, ao tratamento de informações ausentes e ao reforço dos mecanismos de grounding.

A partir dessas observações foi construída uma segunda versão do System Prompt, que demonstrou maior robustez, previsibilidade e aderência aos requisitos definidos para o projeto.

Os resultados obtidos evidenciam a importância da iteração contínua na construção de prompts e demonstram que pequenas alterações estruturadas podem produzir melhorias significativas no comportamento do modelo.

Como resultado final, o System Prompt V2 é considerado adequado para o cenário proposto, atendendo aos guardrails estabelecidos pelo negócio, respeitando as fontes documentais disponíveis e reduzindo riscos relacionados à geração de respostas incorretas ou não fundamentadas.
