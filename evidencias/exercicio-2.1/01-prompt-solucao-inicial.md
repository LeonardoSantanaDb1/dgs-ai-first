Estou participando de uma certificação AI First e atuo no papel de Desenvolvedor.

Preciso resolver o Exercício 2.1 — Configuração de MCP Servers.

## Contexto do projeto

Projeto: **NovaTech Assistant**

Stack técnica:

- TypeScript
- Azure Functions v4
- React
- Vitest
- Zod
- Pino

Objetivo do projeto:

- Estruturar o ambiente para uso de agentes de IA.
- O projeto utiliza **Spec Driven Development — SDD**.
- O repositório possui:
  - specs
  - skills
  - prompts
  - ADRs
  - código-fonte
  - testes

Conceito do exercício:

> MCP, Model Context Protocol, é o protocolo que padroniza como modelos de IA se conectam a ferramentas externas.  
> Um MCP Server expõe três primitivas principais: Tools, Resources e Prompts.

## Estrutura do projeto

Considere a estrutura apresentada no **ANEXO C**.

## Tarefa

Analise o contexto do projeto NovaTech Assistant e produza uma proposta técnica para o Exercício 2.1 — Configuração de MCP Servers.

A resposta deve ser específica para esse projeto, evitando respostas genéricas.

## Para cada MCP Server proposto, identifique obrigatoriamente:

- Nome do MCP Server
- Objetivo
- Tools expostas
- Resources expostos
- Prompts expostos
- Papéis consumidores
- Permissões mínimas, seguindo Least Privilege
- Se deve ser um servidor existente ou customizado
- Justificativa técnica da decisão

## Depois da lista de MCP Servers, produza também:

### 1. Configuração MCP proposta para o projeto

Inclua uma proposta de configuração compatível com o contexto do NovaTech Assistant.

Considere que o projeto usa:

- TypeScript
- Azure Functions v4
- React
- Vitest
- Zod
- Pino
- SDD
- specs, skills, prompts, ADRs, código e testes

A configuração deve indicar quais servidores MCP seriam registrados e qual seria o papel de cada um no fluxo de desenvolvimento com agentes de IA.

### 2. Riscos de segurança específicos do contexto

Identifique riscos concretos, como:

- acesso excessivo ao repositório
- alteração indevida de specs, ADRs ou prompts
- leitura de arquivos sensíveis
- execução de comandos perigosos
- vazamento de dados
- prompt injection em prompts, specs ou documentação
- uso indevido de ferramentas de escrita
- agente modificando código sem testes
- agente ignorando decisões arquiteturais registradas em ADRs

### 3. Mitigações propostas

Para cada risco relevante, proponha mitigação prática.

Considere mecanismos como:

- read-only por padrão
- escrita restrita a diretórios específicos
- allowlist de comandos
- bloqueio de arquivos sensíveis
- validação com Zod
- logs estruturados com Pino
- exigência de testes com Vitest
- revisão humana obrigatória
- segregação entre MCPs de leitura e escrita
- limitação de permissões por papel consumidor
- política de aprovação antes de alterações em specs, ADRs e prompts

### 4. Autoavaliação crítica da própria solução

Faça uma análise crítica da solução proposta.

Aponte possíveis fragilidades, por exemplo:

- excesso de MCPs para um projeto inicial
- risco de complexidade operacional
- dependência de servidores customizados
- dificuldade de manter permissões granulares
- risco de agentes seguirem documentação desatualizada
- necessidade de maturidade do time para operar SDD com agentes
- pontos que deveriam ser validados em um piloto antes da adoção definitiva

## Critérios de qualidade esperados

A resposta deve estar no nível esperado por um Tech Lead experiente.

Considere:

- aderência ao conceito de MCP
- distinção clara entre Tools, Resources e Prompts
- coerência com a estrutura do repositório
- aplicação real de Least Privilege
- justificativa para cada servidor existir
- explicação sobre por que determinados MCPs devem existir e outros não
- foco no papel de Desenvolvedor
- relação com Spec Driven Development
- preocupação com segurança, governança e rastreabilidade
- viabilidade prática para um projeto TypeScript/Azure Functions/React

## Importante

Não quero uma resposta genérica sobre MCP.

Quero uma proposta aplicável ao projeto NovaTech Assistant, considerando que o repositório possui specs, skills, prompts, ADRs, código-fonte e testes.

Organize a resposta em formato de documento técnico, como se fosse o conteúdo final do arquivo:

`exercicio-2.1-mcp-servers.md`