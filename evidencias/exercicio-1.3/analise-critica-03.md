# Análise Crítica 03 - Implementação da Busca Semântica

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04

---

# Objetivo

Avaliar criticamente as decisões técnicas e a implementação propostas pelo Claude para a etapa de busca semântica do pipeline RAG da NovaTech.

O objetivo desta análise é verificar a aderência das recomendações ao escopo da prova de conceito, identificar riscos relevantes e definir quais decisões serão incorporadas à solução.

---

# Avaliação das Recomendações

## 1. Utilização do Mesmo Modelo de Embeddings

### Recomendação

Utilizar exatamente o mesmo modelo de embeddings na ingestão e na busca.

### Decisão

✅ Aceita

### Justificativa

A recomendação é tecnicamente correta.

A recuperação semântica depende da comparação entre vetores gerados dentro do mesmo espaço vetorial.

A utilização de modelos distintos comprometeria diretamente a qualidade da busca e poderia produzir resultados inconsistentes.

A recomendação está alinhada com boas práticas de implementação de sistemas RAG.

---

## 2. Conversão de Distância em Similaridade

### Recomendação

Converter a distância retornada pelo ChromaDB em um valor de similaridade utilizando a fórmula:

```text
similaridade = 1 - distância
```

### Decisão

✅ Aceita

### Justificativa

A recomendação melhora significativamente a interpretação dos resultados durante os testes.

Valores de similaridade são mais intuitivos para análise humana do que distâncias vetoriais.

Além disso, essa abordagem facilita a comparação entre diferentes consultas realizadas durante a validação do pipeline.

---

## 3. Utilização de Top-K = 3

### Recomendação

Utilizar três chunks como configuração padrão de recuperação.

### Decisão

✅ Aceita

### Justificativa

O volume documental da prova de conceito é reduzido e as consultas previstas possuem escopo relativamente específico.

Dessa forma, a recuperação inicial de três chunks representa um equilíbrio adequado entre relevância e simplicidade.

A implementação permanece flexível para ajustes futuros caso os testes indiquem necessidade de recuperação adicional.

---

## 4. Ausência de Re-Ranker

### Recomendação

Não implementar etapa de re-ranking nesta fase.

### Decisão

✅ Aceita

### Justificativa

Embora re-rankers possam melhorar a precisão da recuperação, sua utilização não é necessária para validar os conceitos centrais do exercício.

A inclusão dessa camada aumentaria a complexidade da solução sem gerar benefícios proporcionais para o objetivo atual da prova de conceito.

---

## 5. Interface de Linha de Comando

### Recomendação

Implementar a busca utilizando interface CLI baseada em argparse.

### Decisão

✅ Aceita

### Justificativa

A abordagem simplifica os testes e facilita a validação dos resultados.

Além disso, permite integração futura com os demais componentes do pipeline sem necessidade de interfaces adicionais.

---

## 6. Conflito Entre PROC-042-v1 e PROC-042-v2

### Recomendação

Implementar mecanismos para tratamento de múltiplas versões documentais.

### Decisão

✅ Aceita Parcialmente

### Justificativa

O risco identificado é real.

A coexistência de versões distintas de um mesmo procedimento pode gerar recuperação de informações conflitantes.

Entretanto, o exercício não exige mecanismos avançados de governança documental.

Dessa forma, o risco será registrado como limitação conhecida da prova de conceito e validado durante os testes de recuperação.

Em uma solução produtiva seria recomendável incorporar:

- Controle de vigência documental.
- Metadados de versão.
- Estratégias de filtragem durante a recuperação.

---

# Avaliação da Implementação

## Aderência ao Exercício

A implementação proposta atende aos requisitos definidos para a etapa de busca.

Foram contempladas as funcionalidades de:

- geração de embeddings para perguntas;
- consulta ao ChromaDB;
- recuperação dos chunks mais relevantes;
- exibição de score;
- exibição das fontes recuperadas.

Não foram identificadas funcionalidades fora do escopo solicitado.

---

## Simplicidade da Solução

A implementação mantém baixo acoplamento e reduz complexidade desnecessária.

Essa característica favorece a compreensão do funcionamento interno do pipeline e facilita a geração de evidências para o exercício.

---

## Qualidade da Implementação

A solução proposta demonstra preocupação com:

- rastreabilidade;
- legibilidade;
- facilidade de testes;
- reutilização dos componentes já implementados durante a ingestão.

Essas características são compatíveis com os objetivos da prova de conceito.

---

# Riscos Remanescentes

Mesmo após a implementação da busca, permanecem alguns riscos conhecidos:

- Recuperação simultânea de versões conflitantes de documentos.
- Possível recuperação de chunks semanticamente semelhantes, porém menos relevantes.
- Limitações inerentes ao modelo all-MiniLM-L6-v2 para termos muito específicos do domínio logístico.
- Dependência da qualidade da estratégia de chunking adotada na ingestão.

Esses riscos serão avaliados durante os testes de recuperação previstos nas próximas etapas.

---

# Conclusão

A análise conclui que as decisões técnicas apresentadas pelo Claude são adequadas para os objetivos da prova de conceito e permanecem aderentes ao escopo definido pelo exercício.

As recomendações relacionadas ao uso consistente de embeddings, configuração do Top-K, interpretação dos scores e simplificação arquitetural foram integralmente aceitas.

A preocupação com múltiplas versões documentais foi considerada válida, porém classificada como uma limitação conhecida da prova de conceito, não exigindo implementação imediata.

A implementação da etapa de busca foi considerada adequada para prosseguir com a execução dos testes de recuperação e validação dos resultados do pipeline RAG.