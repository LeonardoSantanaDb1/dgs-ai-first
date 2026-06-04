# Prompt 04 - Implementação da Montagem de Prompt

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04

---

## Objetivo

Solicitar apoio do Claude Code para implementar a etapa de montagem de prompt do pipeline RAG.

---

## Prompt Enviado ao Claude Code

Estou desenvolvendo o Exercício 1.3 da trilha AI First.

A etapa de ingestão já foi implementada e executada com sucesso.

A etapa de busca semântica também já foi implementada e validada.

Agora preciso implementar apenas o arquivo:

```text
src/prompt_builder.py
```

Requisitos:

1. Receber uma pergunta via linha de comando.
2. Reutilizar a lógica de busca semântica já implementada em `search.py`.
3. Recuperar os Top-K chunks mais relevantes.
4. Montar um prompt completo contendo:
   - System Prompt.
   - Chunks recuperados.
   - Pergunta do usuário.
   - Instruções para responder apenas com base no contexto.
5. Exibir o prompt final no terminal.
6. Permitir configurar Top-K com parâmetro opcional.
7. Manter o código simples, legível e adequado para POC.
8. Não usar LangChain.
9. Não implementar chamada automática para API de LLM.
10. O prompt gerado deve ser pronto para copiar e colar manualmente no Claude.

System Prompt esperado:

Você é o Assistente de Atendimento da NovaTech.

Responda utilizando exclusivamente as informações presentes no contexto fornecido.

Regras obrigatórias:
- Sempre cite a fonte do documento utilizado.
- Nunca invente prazos, valores, regras ou procedimentos.
- Se a resposta não estiver presente no contexto, informe que não encontrou informação suficiente.
- Quando não houver evidência suficiente, recomende escalar para o supervisor.
- Responda em português formal e acessível.

Formato esperado da resposta:
Resposta:
[resposta objetiva]

Fonte:
[documento utilizado]

Observações:
[observações relevantes ou exceções]

Antes de gerar o código:
- explique brevemente as decisões técnicas;
- depois gere o código completo do `prompt_builder.py`.