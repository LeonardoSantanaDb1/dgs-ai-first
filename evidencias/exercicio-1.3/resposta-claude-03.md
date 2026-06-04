# Resposta Claude 03 - Implementação da Busca Semântica

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04

---

# Objetivo

Implementar a etapa de busca semântica do pipeline RAG da NovaTech.

O objetivo desta etapa é permitir que perguntas realizadas pelos usuários sejam convertidas em embeddings e utilizadas para recuperar os chunks mais relevantes armazenados no ChromaDB durante a fase de ingestão.

---

# Resposta Gerada pelo Claude

## Análise da Solução

Antes de gerar a implementação, o Claude realizou uma análise técnica da arquitetura existente e apresentou recomendações relacionadas à estratégia de recuperação semântica.

---

# Decisões Técnicas Propostas

## Utilização do Mesmo Modelo de Embeddings

O embedding da pergunta precisa ser gerado pelo mesmo modelo e mesma configuração utilizados durante a ingestão.

Caso documentos e perguntas sejam vetorizados utilizando modelos diferentes, os vetores passarão a existir em espaços semânticos distintos, comprometendo completamente a qualidade da recuperação.

Por esse motivo, o Claude recomendou a utilização da mesma constante de configuração para ambos os processos.

---

## Tratamento de Similaridade

Com a configuração `hnsw:space: cosine`, o ChromaDB retorna distância cosseno e não similaridade.

Nesse modelo:

- 0 representa máxima proximidade.
- Valores maiores representam menor proximidade.

Para facilitar a interpretação dos resultados durante os testes, o Claude sugeriu converter a distância em similaridade através da fórmula:

```text
similaridade = 1 - distância
```

Essa abordagem produz valores mais intuitivos para análise dos resultados.

---

## Configuração do Top-K

Foi sugerida a utilização de:

```text
Top-K = 3
```

como configuração padrão.

Segundo o Claude, três chunks são suficientes para a maior parte das consultas previstas no exercício.

Para consultas mais amplas ou que envolvam múltiplos domínios, o parâmetro poderá ser ajustado para valores superiores.

O Claude alertou que valores muito elevados podem introduzir ruído no contexto e reduzir a qualidade das respostas geradas posteriormente pelo LLM.

---

## Ausência de Re-Ranker

O Claude recomendou manter a recuperação baseada exclusivamente em embeddings para esta prova de conceito.

Foi observado que soluções produtivas normalmente incorporam uma etapa adicional de re-ranking utilizando modelos especializados.

Entretanto, a complexidade adicional não se justifica para os objetivos do exercício.

---

## Interface CLI

Foi proposta uma interface baseada em linha de comando utilizando `argparse`.

Essa abordagem permite:

- Execução simples dos testes.
- Facilidade de validação dos resultados.
- Integração com scripts posteriores.
- Menor complexidade de implementação.

---

# Risco Identificado

## Conflito Entre PROC-042-v1 e PROC-042-v2

### Observação do Claude

Ao executar consultas relacionadas a frete especial, existe a possibilidade de que os documentos:

- PROC-042-v1
- PROC-042-v2

sejam recuperados simultaneamente.

Como ambos permanecem indexados na base vetorial e não existe controle de vigência documental, o mecanismo de recuperação não possui capacidade de determinar qual documento representa a versão atualmente válida.

Isso pode resultar na recuperação de informações conflitantes para uma mesma consulta.

### Exemplo

PROC-042-v1:

```text
Região Norte = 1.6
```

PROC-042-v2:

```text
Região Norte = 1.8
```

Nesse cenário, ambos os documentos podem ser considerados semanticamente relevantes para a mesma pergunta.

### Recomendação

O Claude sugeriu que futuras evoluções da solução considerem:

- Metadados de vigência documental.
- Controle de versão.
- Filtros documentais durante a recuperação.

---

# Implementação Gerada

Arquivo:

```text
src/search.py
```

Responsabilidades implementadas:

- Receber perguntas via linha de comando.
- Gerar embeddings utilizando o modelo all-MiniLM-L6-v2.
- Conectar ao ChromaDB persistido localmente.
- Consultar a coleção vetorial criada durante a ingestão.
- Recuperar os chunks mais similares.
- Exibir score de similaridade.
- Exibir documento de origem.
- Exibir índice do chunk recuperado.
- Exibir conteúdo dos chunks retornados.
- Permitir configuração do parâmetro Top-K.

---

# Resultado Esperado

A implementação deverá permitir validar a qualidade da recuperação semântica do pipeline RAG.

Os testes previstos incluem consultas relacionadas a:

- Política de devolução.
- SLA de clientes.
- Frete especial.
- Perguntas presentes no mapa de cobertura do exercício.

A expectativa é que os chunks recuperados correspondam aos documentos indicados pelo gabarito disponibilizado no Anexo B.

---

# Benefícios da Implementação

A solução proposta apresenta os seguintes benefícios:

- Simplicidade de execução.
- Baixa complexidade operacional.
- Reutilização da infraestrutura criada na ingestão.
- Facilidade de interpretação dos resultados.
- Adequação ao escopo da prova de conceito.

Além disso, a implementação fornece informações suficientes para avaliar a qualidade da recuperação antes da integração com o modelo de linguagem.

---

# Próximos Passos

Após a implementação do search.py serão executadas consultas reais utilizando perguntas do domínio da NovaTech.

Os resultados obtidos serão utilizados para:

- Validar a qualidade da recuperação.
- Comparar os resultados com o gabarito do exercício.
- Identificar problemas de recuperação.
- Avaliar a estratégia de chunking adotada.
- Propor melhorias para o pipeline.

A próxima etapa consiste na execução dos testes de busca semântica e análise dos resultados recuperados.