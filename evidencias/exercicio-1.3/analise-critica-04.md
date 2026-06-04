# Análise Crítica 04 - Implementação da Montagem de Prompt

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04

---

# Objetivo

Avaliar criticamente as decisões técnicas e a implementação propostas pelo Claude para a etapa de montagem de prompt do pipeline RAG da NovaTech.

O objetivo desta análise é verificar a aderência da solução aos requisitos do exercício, avaliar os benefícios arquiteturais da abordagem proposta e identificar possíveis limitações para cenários futuros.

---

# Avaliação das Recomendações

## 1. Reutilização da Busca Semântica

### Recomendação

Reutilizar diretamente as funções implementadas em `search.py`, evitando duplicação de código.

### Decisão

✅ Aceita

### Justificativa

A recomendação está alinhada com boas práticas de engenharia de software.

A reutilização reduz duplicidade de lógica, melhora a manutenção da solução e garante consistência entre os componentes do pipeline.

Além disso, eventuais correções realizadas na camada de recuperação passam a beneficiar automaticamente a etapa de montagem do prompt.

---

## 2. Separação Entre Contexto Estático e Contexto Dinâmico

### Recomendação

Separar explicitamente os componentes estáticos e dinâmicos do contexto.

### Decisão

✅ Aceita

### Justificativa

Essa recomendação representa um dos conceitos centrais abordados pelo exercício.

A separação permite isolar regras de comportamento do assistente das informações recuperadas durante cada consulta.

Essa abordagem melhora a governança do prompt e facilita futuras evoluções do sistema.

Além disso, demonstra aplicação prática dos conceitos de Engenharia de Contexto discutidos nas etapas anteriores.

---

## 3. Utilização de Delimitadores de Contexto

### Recomendação

Utilizar marcadores explícitos para delimitar os documentos recuperados.

### Decisão

✅ Aceita

### Justificativa

Os delimitadores aumentam a clareza estrutural do prompt e reduzem ambiguidades durante a interpretação pelo modelo de linguagem.

Essa prática é especialmente importante em cenários onde múltiplos documentos são recuperados simultaneamente.

A recomendação contribui para reduzir o risco de mistura entre instruções do sistema e conteúdo documental.

---

## 4. Estimativa de Tokens

### Recomendação

Exibir uma estimativa aproximada do tamanho do prompt gerado.

### Decisão

✅ Aceita

### Justificativa

Embora a implementação utilize uma aproximação simples, a funcionalidade é suficiente para os objetivos da prova de conceito.

A visualização do tamanho do contexto facilita a compreensão dos impactos do aumento de Top-K e reforça conceitos relacionados ao orçamento de contexto.

Em ambientes produtivos seria recomendável utilizar mecanismos de contagem mais precisos.

---

## 5. Parametrização do Top-K

### Recomendação

Permitir configuração dinâmica da quantidade de chunks recuperados.

### Decisão

✅ Aceita

### Justificativa

A parametrização oferece flexibilidade para realização de testes e análises comparativas.

Diferentes tipos de consulta podem demandar diferentes volumes de contexto.

A implementação mantém simplicidade operacional sem comprometer a capacidade de experimentação.

---

## 6. Diagnóstico Opcional dos Chunks

### Recomendação

Implementar exibição opcional dos chunks recuperados e seus scores.

### Decisão

✅ Aceita

### Justificativa

A funcionalidade possui grande valor para observabilidade e validação do pipeline.

Durante a execução dos testes foi possível identificar problemas reais de ranking e recuperação graças à visualização dos resultados retornados pelo mecanismo vetorial.

A recomendação contribui diretamente para a capacidade de diagnóstico da solução.

---

# Avaliação da Implementação

## Aderência ao Exercício

A implementação atende integralmente aos requisitos definidos para a etapa de montagem de prompt.

Foram contemplados:

- recuperação de contexto;
- utilização do System Prompt;
- composição entre contexto estático e dinâmico;
- geração do prompt final;
- preparação do contexto para envio ao modelo de linguagem.

Não foram identificadas funcionalidades fora do escopo solicitado.

---

## Organização Arquitetural

A solução mantém separação clara entre responsabilidades.

Cada componente do pipeline possui um papel bem definido:

| Componente | Responsabilidade |
|------------|------------------|
| ingest.py | Ingestão e indexação |
| search.py | Recuperação semântica |
| prompt_builder.py | Construção do contexto |

Essa organização reduz acoplamento e facilita manutenção futura.

---

## Engenharia de Contexto

A implementação demonstra compreensão prática dos conceitos de Engenharia de Contexto abordados durante o exercício.

Foi possível identificar claramente:

- Contexto estático.
- Contexto dinâmico.
- Ordem de composição.
- Delimitação das informações.
- Controle do tamanho do contexto.

Esses elementos representam aspectos fundamentais para construção de sistemas RAG em ambiente produtivo.

---

# Riscos Remanescentes

Apesar da qualidade da solução proposta, alguns riscos permanecem presentes.

## Recuperação de Documentos Não Priorizados

O prompt_builder depende diretamente da qualidade dos resultados fornecidos pela etapa de busca.

Problemas de ranking identificados anteriormente continuam impactando o contexto final montado.

---

## Ausência de Controle de Autoridade Documental

O mecanismo atual não diferencia documentos normativos de documentos auxiliares.

Isso pode resultar na inclusão de informações menos relevantes no contexto enviado ao modelo.

---

## Ausência de Controle de Vigência

Documentos com múltiplas versões continuam coexistindo na base vetorial.

Sem mecanismos adicionais de governança documental, versões antigas podem ser incorporadas ao contexto recuperado.

---

# Conclusão

A análise conclui que a implementação proposta pelo Claude é adequada para os objetivos da prova de conceito e apresenta aderência aos requisitos definidos pelo exercício.

As decisões relacionadas à reutilização de componentes, separação entre contexto estático e dinâmico, delimitação explícita do contexto e parametrização do Top-K foram consideradas tecnicamente corretas e foram integralmente aceitas.

A implementação demonstra entendimento consistente dos conceitos de Engenharia de Contexto e completa a construção do pipeline RAG proposto para a NovaTech.

Os riscos identificados estão relacionados principalmente à qualidade da recuperação semântica e não à etapa de montagem de prompt, indicando que a solução encontra-se pronta para validação ponta a ponta utilizando um modelo de linguagem.