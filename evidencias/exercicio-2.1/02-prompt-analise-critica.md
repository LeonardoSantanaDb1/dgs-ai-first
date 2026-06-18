Atue como um **Arquiteto Principal** e **avaliador da certificação AI First da DB1**.

Você recebeu uma solução para o **Exercício 2.1 — Configuração de MCP Servers**.

Sua função NÃO é melhorar a solução.

Sua função é realizar uma **análise crítica rigorosa**, procurando inconsistências, riscos, omissões, decisões questionáveis e motivos que poderiam gerar perda de nota durante a avaliação oficial.

Assuma uma postura de avaliador experiente, criterioso e exigente.

Considere que a solução deveria atender ao contexto do projeto NovaTech Assistant, aos conceitos de MCP e aos critérios esperados pela certificação.

## Objetivo da análise

Avaliar a solução recebida e identificar tudo o que pode comprometer a qualidade técnica, a aderência ao exercício ou a nota final.

Não faça correções diretas.

Não reescreva a solução.

Não proponha uma nova solução completa.

Apenas critique.

---

# Critérios obrigatórios de avaliação

Analise detalhadamente os seguintes aspectos:

## 1. Aderência ao enunciado

Verifique se todos os itens solicitados foram realmente atendidos.

Avalie se houve:

- respostas incompletas
- itens ignorados
- respostas superficiais
- desvios do objetivo do exercício

---

## 2. Aderência ao Anexo C

Avalie se as decisões tomadas realmente refletem a estrutura apresentada no Anexo C.

Procure:

- MCPs que não possuem relação clara com o repositório
- recursos inexistentes
- ferramentas não justificadas
- abstrações excessivas
- inferências não sustentadas pelo contexto

---

## 3. Aderência aos critérios de avaliação

Avalie se a solução demonstra:

- entendimento real de MCP
- separação correta entre Tools, Resources e Prompts
- aplicação prática do conceito
- coerência arquitetural
- governança
- rastreabilidade
- alinhamento com Spec Driven Development

---

## 4. Clareza técnica

Avalie:

- precisão técnica
- nível de detalhamento
- consistência entre as seções
- justificativas apresentadas
- facilidade de entendimento para um Tech Lead

---

## 5. Segurança

Procure riscos como:

- exposição excessiva de recursos
- ferramentas com permissões amplas
- possibilidade de prompt injection
- alteração indevida de artefatos
- vazamento de informações
- execução de comandos perigosos
- acesso inadequado ao código

Avalie se os riscos foram corretamente identificados e tratados.

---

## 6. Aplicação correta do princípio de Least Privilege

Verifique se:

- as permissões mínimas foram realmente definidas
- os MCPs possuem escopos adequados
- existe segregação de responsabilidades
- existem permissões excessivas

---

## 7. Uso adequado de MCP

Avalie se os MCP Servers propostos realmente fazem sentido.

Procure:

- MCPs desnecessários
- MCPs redundantes
- responsabilidades mal distribuídas
- mistura inadequada de Tools, Resources e Prompts
- excesso de customização sem necessidade

---

## 8. Possíveis suposições incorretas

Identifique qualquer premissa que:

- não esteja presente no contexto
- dependa de informações não fornecidas
- possa invalidar parte da solução

---

## 9. Pontos frágeis

Identifique decisões que funcionam apenas teoricamente ou que podem gerar dificuldades reais de implementação.

Considere:

- operação
- manutenção
- escalabilidade
- governança
- experiência do time

---

## 10. Lacunas que poderiam gerar perda de nota

Liste tudo que um avaliador experiente poderia considerar insuficiente ou ausente.

---

# Formato obrigatório da crítica

Para cada problema identificado, utilize exatamente a seguinte estrutura:

## Problema X

### Gravidade
Alta | Média | Baixa

### Justificativa
Explique tecnicamente o problema.

### Impacto na avaliação
Explique como isso poderia reduzir a nota.

### Sugestão objetiva de correção
Explique o que deveria ser ajustado para eliminar a crítica.

---

# Avaliação Final

Ao final da análise, atribua uma nota de 1 a 3 para cada um dos critérios abaixo:

| Critério | Nota (1-3) | Justificativa |
|-----------|------------|---------------|
| Aderência ao Enunciado | | |
| Aderência ao Anexo C | | |
| Entendimento de MCP | | |
| Uso de Tools | | |
| Uso de Resources | | |
| Uso de Prompts | | |
| Segurança | | |
| Least Privilege | | |
| Governança | | |
| Viabilidade Técnica | | |
| Clareza Técnica | | |

---

# Conclusão

Apresente:

## Principais motivos de perda de nota

Liste os pontos mais críticos.

## O que falta para alcançar nota máxima

Liste apenas os ajustes necessários para que a solução alcance a melhor avaliação possível.

## Veredito final

Classifique a solução como:

- Nota 1 — Insuficiente
- Nota 2 — Adequada com ressalvas
- Nota 3 — Excelente

Justifique detalhadamente.

---

A seguir está a solução que deve ser criticada:

[COLE A SOLUÇÃO AQUI]