# Resposta Claude - Iteração 2

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04  

--- 

## Objetivo da Revisão

Revisão técnica formal da análise de viabilidade para aprovação de arquitetura de um sistema RAG corporativo para a NovaTech.

---

# Parecer de Revisão Técnica

Avalio o documento na postura de um gate de aprovação arquitetural.

Meu objetivo é identificar riscos que possam comprometer a implantação em produção e não apenas validar os pontos positivos da proposta.

---

# Pontos Fortes

| ID | Ponto | Justificativa |
|----|--------|--------------|
| F1 | Escolha de RAG sobre Fine-Tuning | Adequada para uma base documental dinâmica, atualizada mensalmente e distribuída em múltiplas fontes. |
| F2 | Foco em Retrieval e Contexto | Demonstra entendimento de que a maior parte das falhas ocorre no pipeline de recuperação e não na geração. |
| F3 | Estratégia diferenciada por tipo de fonte | PDFs, Confluence e planilhas possuem características distintas e exigem abordagens específicas. |
| F4 | Tratamento estruturado para planilhas | Evita o anti-pattern de vetorização indiscriminada de dados tabulares complexos. |
| F5 | Reconhecimento de Lost in the Middle | Demonstra compreensão das limitações relacionadas ao orçamento de atenção dos modelos. |
| F6 | Transparência das hipóteses | A análise explicita premissas e dependências do discovery. |

---

# Riscos Críticos

## C1 - Ausência de Controle de Acesso (ACL)

### Problema

A análise não contempla mecanismos de propagação de permissões do SharePoint para o índice vetorial.

### Impacto

Risco de exposição de documentos restritos para usuários sem autorização.

### Criticidade

**Crítica**

---

## C2 - Ausência de Estratégia de Avaliação

### Problema

Não foram definidos:

- Golden Dataset
- Métricas de qualidade
- Critérios de aceite
- Processo de validação contínua

### Impacto

Impossibilidade de comprovar qualidade ou detectar regressões.

### Criticidade

**Crítica**

---

## C3 - Contradições Documentais sem Resolução

### Problema

O documento reconhece a existência de documentos conflitantes, mas não apresenta mecanismos de resolução.

### Impacto

O sistema poderá recuperar informações contraditórias e responder de forma inconsistente.

### Criticidade

**Crítica**

---

## C4 - Ausência de Estratégia de Grounding

### Problema

Não foi definida política de:

- Citação obrigatória
- Respostas fundamentadas
- Abstenção quando não houver evidência suficiente

### Impacto

Maior risco de alucinação.

### Criticidade

**Crítica**

---

## C5 - Embeddings Não Especificados

### Problema

A análise não define:

- Modelo de embedding
- Critérios de escolha
- Compatibilidade com português

### Impacto

A qualidade do retrieval pode ser comprometida.

### Criticidade

**Crítica**

---

# Riscos Altos

## A1 - Estratégia de Chunking Potencialmente Contraditória

A combinação entre:

- Chunking semântico
- Chunks fixos entre 400 e 600 tokens

pode gerar conflitos em documentos com seções extensas.

---

## A2 - Tabelas de Frete

O armazenamento estruturado aparece apenas como recomendação opcional.

Segundo a revisão, deveria ser tratado como requisito obrigatório.

---

## A3 - Fluxogramas como Imagem

A análise não apresentou estratégia para processamento multimodal de fluxogramas.

---

## A4 - Atualização Incremental

Foi mencionado reprocessamento frequente, porém sem detalhamento sobre:

- CDC
- Effective Dating
- Remoção de versões antigas

---

## A5 - Premissas Otimistas

As hipóteses apresentadas podem não se confirmar durante o discovery.

---

## A6 - Ausência de Query Understanding

Não há estratégia para:

- Query Expansion
- Query Rewriting
- Desambiguação

---

# Riscos Médios

## M1 - Estimativa de Tokens

A revisão aponta que a estimativa baseada em:

```text
0,75 palavras por token
```

é mais aderente ao inglês do que ao português.

---

## M2 - Context Window

O cálculo não reservou explicitamente espaço para:

- Histórico da conversa
- Resposta do modelo

---

## M3 - Macros do Confluence

A análise não detalha a ingestão de macros dinâmicas.

---

## M4 - Custos Operacionais

Não foi apresentada avaliação de:

- Custo de inferência
- Reindexação
- Azure AI Search

---

## M5 - Latência

Não há decomposição do tempo de resposta por etapa.

---

## M6 - Reranking

A análise cita reranking, mas não especifica tecnologia ou estratégia.

---

## M7 - Quantidade de Planilhas

O número de aproximadamente 50 planilhas não consta explicitamente no cenário.

---

# Riscos Baixos

| ID | Observação |
|----|------------|
| B1 | LGPD e residência de dados não foram mencionadas. |
| B2 | Dependência de um único modelo. |
| B3 | Observabilidade pouco detalhada. |
| B4 | GPT-4o tratado como única opção. |
| B5 | Overlap fixo de 10% pode não funcionar igualmente bem em todos os documentos. |

---

# Recomendações de Melhoria

## Segurança

Implementar:

- ACL
- Security Trimming
- Integração com Entra ID

---

## Avaliação

Construir um Golden Dataset contendo perguntas reais de atendimento.

Definir métricas de:

- Faithfulness
- Context Recall
- Context Precision
- Taxa de Citação Correta

---

## Governança

Implementar:

- Fonte única da verdade
- Controle de vigência
- Effective Dating
- Hierarquia de autoridade documental

---

## Grounding

Implementar:

- Citação obrigatória
- Política de abstenção
- Respostas baseadas apenas em conteúdo recuperado

---

## Embeddings

Selecionar e validar modelo compatível com PT-BR.

---

## Chunking

Avaliar:

- Parent-Child Retrieval
- Late Chunking
- Recuperação hierárquica

---

## Dados Estruturados

Tabelas de frete e SLA devem ser tratadas como dados estruturados e não apenas como documentos vetoriais.

---

## Fluxogramas

Implementar pipeline multimodal para interpretação de diagramas e imagens.

---

## Atualização da Base

Implementar:

- Indexação incremental
- Controle de versões
- Remoção de documentos obsoletos

---

# Avaliação Geral

| Critério | Avaliação |
|-----------|-----------|
| Domínio Conceitual | Bom |
| Engenharia de Contexto | Boa |
| Chunking | Bom |
| Retrieval | Bom |
| Prontidão para Produção | Insuficiente |
| Segurança | Insuficiente |
| Governança | Insuficiente |
| Avaliação de Qualidade | Insuficiente |

---

# Veredito

**Não aprovado para produção na forma atual.**

A análise apresenta boa fundamentação conceitual sobre RAG, chunking, retrieval e gerenciamento de contexto.

Entretanto, a ausência de estratégias explícitas para:

- Segurança
- Governança documental
- Avaliação da qualidade
- Grounding
- Resolução de contradições

impede sua aprovação como arquitetura pronta para ambiente corporativo de produção.

A recomendação é prosseguir com o discovery, validando empiricamente as hipóteses levantadas e incorporando os controles necessários antes do go-live.
