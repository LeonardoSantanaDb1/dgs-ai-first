Atue como **Arquiteto Principal**, **Tech Lead Sênior** e **avaliador oficial da certificação AI First da DB1**.

Você recebeu uma solução para o **Exercício 2.3 — Definição de Estratégia de Skills**.

Sua função NÃO é melhorar a solução.

Sua função é realizar uma **análise crítica rigorosa**, procurando inconsistências, omissões, decisões questionáveis, fragilidades arquiteturais e motivos que poderiam gerar perda de nota durante a avaliação oficial.

Assuma uma postura de avaliador experiente, criterioso e exigente.

Não seja complacente.

Procure ativamente motivos para descontar pontos.

---

# Objetivo da análise

Avaliar se a solução realmente atende aos objetivos do Exercício 2.3 e aos princípios de engenharia de contexto, Skills e Spec Driven Development.

Não reescreva a solução.

Não produza uma nova árvore de Skills.

Não gere uma versão corrigida.

Apenas critique.

---

# Critérios obrigatórios de avaliação

## 1. Aderência ao enunciado

Verifique se todos os itens solicitados foram realmente atendidos.

Avalie se houve:

- respostas incompletas
- ausência de justificativas
- campos preenchidos superficialmente
- desvios do objetivo do exercício

---

## 2. Aderência ao Anexo C

Avalie se as Skills propostas realmente refletem:

- a estrutura do repositório
- os artefatos existentes
- o fluxo de trabalho esperado
- a stack tecnológica
- a organização Foundation / Domain / Artifact

Questione qualquer Skill que pareça desconectada do contexto.

---

## 3. Coerência da árvore Foundation → Domain → Artifact

Avalie se a árvore respeita o papel de cada categoria.

Verifique:

### Foundation

- conhecimentos transversais
- padrões globais
- convenções reutilizáveis

### Domain

- conhecimento específico do negócio ou arquitetura do projeto

### Artifact

- geração ou manutenção de artefatos específicos

Procure Skills classificadas na categoria errada.

---

## 4. Utilidade real das Skills propostas

Questione se cada Skill:

- resolve um problema concreto
- reduz ambiguidade
- melhora a qualidade das entregas
- seria efetivamente utilizada por agentes

Identifique Skills decorativas ou artificiais.

---

## 5. Skills faltantes

Avalie se existe alguma lacuna importante.

Considere:

- TypeScript
- React
- Azure Functions
- Vitest
- Zod
- Pino
- SDD
- ADRs
- prompts
- engenharia de contexto
- arquitetura

Identifique Skills que deveriam existir e não foram propostas.

---

## 6. Skills redundantes

Avalie se existem Skills que:

- se sobrepõem
- duplicam responsabilidades
- poderiam ser consolidadas

Procure fragmentação excessiva.

---

## 7. Escolha da Skill Foundation mais importante

Analise criticamente a Skill escolhida.

Questione se ela realmente é a Skill mais importante do projeto.

Considere especialmente:

### error-handling.md

e

### typescript-conventions.md

Avalie:

- qual delas possui maior impacto transversal
- qual reduz mais erros
- qual influencia mais agentes
- qual serve de base para mais decisões

Não aceite a escolha sem justificativa forte.

---

## 8. Qualidade do SKILL.md

Avalie se o arquivo produzido seria realmente útil para um agente.

Verifique:

### Contexto

Está claro e específico?

### Regras prescritivas

São objetivas e verificáveis?

### Dependências

São coerentes?

---

## 9. Avaliação dos exemplos DO / DON'T

Verifique:

- aderência ao contexto NovaTech Assistant
- aderência à stack
- aplicabilidade prática
- clareza

Questione exemplos genéricos.

---

## 10. Avaliação dos Anti-patterns

Verifique se os anti-patterns:

- são reais
- são frequentes
- são relevantes para o projeto
- ajudam efetivamente um agente

Questione anti-patterns superficiais.

---

# Atenção especial

Dedique uma seção exclusiva para responder:

## A Skill detalhada deveria realmente ser error-handling.md?

Compare explicitamente com:

### typescript-conventions.md

Avalie:

- impacto arquitetural
- frequência de uso
- influência sobre outras Skills
- relevância para o papel Desenvolvedor
- alinhamento com a certificação

Explique qual delas possui maior potencial de maximizar a nota do exercício.

---

# Formato obrigatório da crítica

Para cada problema identificado utilize exatamente a estrutura abaixo:

## Problema X

### Gravidade
Alta | Média | Baixa

### Justificativa

Explique tecnicamente o problema.

### Impacto na avaliação

Explique como isso pode reduzir a nota.

### Sugestão objetiva de correção

Explique o que deveria ser ajustado.

---

# Avaliação Final

Atribua nota de 1 a 3 para cada critério abaixo:

| Critério | Nota (1-3) | Justificativa |
|-----------|------------|---------------|
| Aderência ao Enunciado | | |
| Aderência ao Anexo C | | |
| Estrutura Foundation | | |
| Estrutura Domain | | |
| Estrutura Artifact | | |
| Utilidade das Skills | | |
| Governança | | |
| Engenharia de Contexto | | |
| Qualidade do SKILL.md | | |
| Escolha da Skill Principal | | |
| Clareza Técnica | | |

---

# Conclusão

Apresente:

## Principais motivos de perda de nota

Liste os pontos mais críticos.

## O que falta para alcançar nota máxima

Liste apenas os ajustes necessários.

## Veredito Final

Classifique a solução como:

- Nota 1 — Insuficiente
- Nota 2 — Adequada com ressalvas
- Nota 3 — Excelente

Justifique detalhadamente.
