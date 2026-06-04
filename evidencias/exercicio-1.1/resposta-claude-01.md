# Resposta Claude - Iteração 01

**Nome:** Leonardo Santana 
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-01

---

## Observação Inicial

Antes de entrar na análise, uma observação estratégica que atravessa todo o caso e que um arquiteto sênior precisa colocar na mesa logo no início:

O problema central da NovaTech não é apenas de retrieval, mas de governança de conteúdo.

A frase:

> "A equipe resolve perguntando para quem sabe"

indica que atualmente não existe uma fonte única de verdade. Existem documentos contraditórios e a resolução dessas divergências acontece através do conhecimento tácito dos colaboradores.

Um sistema RAG reproduz fielmente a base de conhecimento que recebe. Portanto, se a base contiver informações conflitantes, o assistente poderá produzir respostas diferentes para a mesma pergunta, aumentando o risco operacional por transmitir essas respostas com a autoridade de um sistema oficial.

Esse problema precisa ser tratado não apenas no pipeline técnico, mas também na governança documental da organização.

---

# 1. Análise por Tipo de Fonte Documental

## 1.1 SharePoint — PDFs e Word (~800 documentos)

| Dimensão | Detalhamento |
|-----------|-------------|
| **Desafios de ingestão** | PDFs nativos convivem com documentos escaneados que exigem OCR. Existem tabelas de frete com mais de 15 colunas, fluxogramas embutidos como imagens, documentos Word com comentários, track changes, cabeçalhos e rodapés. Há também o desafio de identificar a versão autoritativa de cada documento. |
| **Impacto na qualidade das respostas** | Alto risco operacional. Tabelas convertidas incorretamente podem gerar interpretações erradas de valores. OCR com erros pode alterar números críticos. Fluxogramas não processados resultam em respostas incompletas. |
| **Estratégias de mitigação** | Utilizar Azure AI Document Intelligence para extração estruturada. Aplicar chunking específico para tabelas. Migrar tabelas críticas para armazenamento estruturado. Utilizar OCR com score de confiança e governança de versão baseada em documentos publicados e vigentes. |

---

## 1.2 Confluence — Wiki Interna (~400 páginas)

| Dimensão | Detalhamento |
|-----------|-------------|
| **Desafios de ingestão** | Macros customizadas, links internos, hierarquia entre páginas e conteúdo distribuído entre documentos relacionados. |
| **Impacto na qualidade das respostas** | Links quebrados podem gerar respostas incompletas. Perda da hierarquia pode causar ambiguidades de contexto. |
| **Estratégias de mitigação** | Ingestão através da API REST do Confluence utilizando conteúdo renderizado. Preservação de metadados hierárquicos. Construção de grafo de relacionamentos para suportar consultas multi-hop. |

---

## 1.3 Planilhas de Referência (~50 arquivos)

| Dimensão | Detalhamento |
|-----------|-------------|
| **Desafios de ingestão** | Fórmulas interdependentes, múltiplas abas, tabelas dinâmicas e atualização periódica. |
| **Impacto na qualidade das respostas** | Alto risco de perda de contexto caso a planilha seja convertida apenas para texto. O modelo pode alucinar valores ou interpretar incorretamente regras de negócio. |
| **Estratégias de mitigação** | Tratar planilhas como dados estruturados. Realizar ETL para Azure SQL. Utilizar Function Calling ou consultas estruturadas em vez de RAG textual para dados tabulares críticos. |

---

# 2. Riscos Técnicos do Pipeline RAG

| Risco | Descrição | Severidade | Mitigação |
|---------|------------|------------|------------|
| Extração parcial silenciosa | Falhas de OCR ou parsing não detectadas | Alta | Métricas de cobertura e validação pós-ingestão |
| Chunking inadequado | Tabelas e procedimentos quebrados entre chunks | Alta | Chunking semântico e parent-child retrieval |
| Limitações de embeddings | Termos específicos do domínio podem ser mal representados | Média-Alta | Embeddings multilíngues e retrieval híbrido |
| Drift do índice | Base desatualizada em relação aos documentos vigentes | Alta | Sincronização incremental |
| Documentos contraditórios | Recuperação simultânea de versões conflitantes | Crítica | Governança documental e controle de vigência |
| Segurança e ACL | Exposição indevida de documentos restritos | Crítica | Security Trimming baseado em Entra ID |
| Alucinação | Respostas sem fundamento documental | Alta | Grounding obrigatório e citações de fonte |

---

# 3. Riscos Relacionados à Engenharia de Contexto

| Risco | Descrição | Mitigação |
|---------|------------|------------|
| Orçamento da Janela de Contexto | Chunks, histórico e instruções competem pelo mesmo espaço | Definir orçamento de tokens por componente |
| Lost in the Middle | Informações relevantes posicionadas no meio do contexto recebem menos atenção | Reordenar chunks por relevância |
| Trade-off de Chunk Size | Chunks pequenos fragmentam contexto e chunks grandes desperdiçam atenção | Chunking adaptativo |
| Over Stuffing | Excesso de chunks reduz qualidade das respostas | Limitar Top-K e aplicar reranking |
| Histórico Multi-turn | Conversas longas degradam qualidade | Sumarização e janela deslizante |
| Contexto Conflitante | Chunks contraditórios são enviados simultaneamente | Priorização por vigência e autoridade |

---

# 4. Riscos Relacionados ao Retrieval

| Risco | Descrição | Mitigação |
|---------|------------|------------|
| Mismatch Léxico × Semântico | Busca vetorial não encontra termos exatos | Retrieval híbrido (BM25 + Vetorial) |
| Gap de Vocabulário | Usuário usa termos diferentes dos documentos | Query Expansion |
| Recall × Precisão | Poucos chunks perdem contexto; muitos chunks geram ruído | Reranking |
| Consultas Multi-Hop | Respostas exigem combinação de múltiplos documentos | Recuperação iterativa |
| Recência | Versões antigas competem com versões atuais | Ranking temporal |
| Consulta Tabular | Busca vetorial é inadequada para lookup exato | SQL ou Function Calling |

---

# 5. Recomendações Arquiteturais

## 5.1 Arquitetura de Referência

| Camada | Componente Recomendado | Função |
|----------|------------------------|---------|
| Ingestão | Azure AI Document Intelligence | OCR e extração estruturada |
| Multimodal | GPT-4o Vision | Processamento de fluxogramas |
| Indexação | Azure AI Search | Índice híbrido vetorial + keyword |
| Dados Estruturados | Azure SQL | Consulta de frete e SLA |
| Retrieval | Azure AI Search + Semantic Ranker | Recuperação e reranking |
| Orquestração | Azure OpenAI + Semantic Kernel | Montagem de contexto |
| Interface | Microsoft Teams | Canal de atendimento |
| Segurança | Microsoft Entra ID | Controle de acesso |
| Observabilidade | Azure Monitor | Auditoria e métricas |

---

## 5.2 Governança de Conteúdo

| Ação | Justificativa |
|--------|---------------|
| Definir fonte única da verdade | Eliminar contradições |
| Controlar vigência documental | Priorizar versões corretas |
| Processo unificado de revisão | Reduzir inconsistências |
| Detecção automática de conflitos | Evitar respostas divergentes |

---

## 5.3 Planejamento de Alto Nível

| Fase | Objetivo |
|---------|---------|
| Mês 1 | Discovery, auditoria documental e definição da governança |
| Mês 2 | Construção do MVP com SharePoint, Azure AI Search e Teams |
| Mês 3 | Integração Confluence, planilhas, OCR avançado e Go-Live |

---

# Conclusão

O principal risco do projeto não está na tecnologia de IA Generativa ou na implementação do RAG, mas na qualidade e governança da documentação existente.

A meta de reduzir o tempo médio de busca de 12 minutos para menos de 2 minutos é tecnicamente viável.

Entretanto, a consistência das respostas dependerá diretamente da capacidade da organização de resolver conflitos documentais, estabelecer uma fonte única de verdade e manter um processo contínuo de atualização e governança da base de conhecimento.