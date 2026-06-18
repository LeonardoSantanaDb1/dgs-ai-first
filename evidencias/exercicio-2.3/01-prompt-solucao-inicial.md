Atue como um Arquiteto de Soluções Sênior, especialista em AI First, Spec Driven Development, engenharia de contexto e definição de Skills para agentes de IA.

Estou participando de uma certificação AI First e atuo no papel de Desenvolvedor.

Preciso resolver o Exercício 2.3 — Definição de Estratégia de Skills.

# Contexto do projeto

Projeto: NovaTech Assistant

Stack técnica:

- TypeScript
- Azure Functions v4
- React
- Vitest
- Zod
- Pino

O projeto utiliza Spec Driven Development — SDD.

O repositório possui estrutura de Skills organizada em:

- `/skills/foundation`
- `/skills/domain`
- `/skills/artifact`

Considere também a estrutura do repositório apresentada no Anexo C.

# Objetivo do exercício

Definir a árvore completa de Skills do projeto NovaTech Assistant.

Para cada Skill, identifique obrigatoriamente:

- Nome
- Categoria: Foundation, Domain ou Artifact
- Objetivo
- Descrição ou frase de ativação
- Quem cria
- Quem consome
- Frequência de uso
- Dependências
- Justificativa arquitetural para sua existência

# Tarefas obrigatórias

## 1. Propor a árvore completa de Skills

Organize a árvore respeitando a estrutura:

```text
skills/
├── foundation/
├── domain/
└── artifact/