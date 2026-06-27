/**
 * response-validator.ts
 *
 * Responsável por validar o Structured Output do modelo de linguagem
 * e aplicar guardrails determinísticos antes de expor respostas ao atendente.
 *
 * Módulo: src/services/response-validator.ts
 * Projeto: NovaTech Assistant — AI First Certification (Exercício 3.1)
 */

import { z } from "zod";
import pino from "pino";

// ---------------------------------------------------------------------------
// Logger
// ---------------------------------------------------------------------------

const logger = pino({
  name: "response-validator",
  level: process.env.LOG_LEVEL ?? "info",
});

// ---------------------------------------------------------------------------
// Schema Zod — Structured Output do modelo
// ---------------------------------------------------------------------------

/**
 * Representa a estrutura exata que o modelo deve retornar.
 * Qualquer desvio causa rejeição imediata pelo schema.
 *
 * `.strict()` rejeita objetos com propriedades não declaradas,
 * garantindo que o Structured Output não carregue campos extras
 * que possam indicar desvio do contrato definido com o modelo.
 */
export const ModelResponseSchema = z
  .object({
    /**
     * Resposta gerada pelo modelo para o atendente.
     * Strings contendo apenas espaços em branco são consideradas inválidas.
     */
    answer: z
      .string()
      .min(1, "O campo 'answer' não pode estar vazio.")
      .refine((v) => v.trim().length > 0, {
        message: "O campo 'answer' não pode conter apenas espaços em branco.",
      }),

    /**
     * Documento fonte utilizado pelo RAG para embasar a resposta.
     * Deve ser uma string não-vazia — ausência indica resposta sem grounding.
     * Strings contendo apenas espaços em branco são consideradas inválidas.
     */
    source_document: z
      .string()
      .min(1, "O campo 'source_document' não pode estar vazio.")
      .refine((v) => v.trim().length > 0, {
        message:
          "O campo 'source_document' não pode conter apenas espaços em branco.",
      }),

    /**
     * Grau de confiança do modelo sobre a resposta, de 0.0 a 1.0.
     * Valores fora desse intervalo indicam problema no pipeline.
     */
    confidence_score: z
      .number()
      .min(0, "confidence_score deve ser >= 0.")
      .max(1, "confidence_score deve ser <= 1."),
  })
  .strict();

/** Tipo TypeScript inferido do schema — sem 'any'. */
export type ModelResponse = z.infer<typeof ModelResponseSchema>;

// ---------------------------------------------------------------------------
// Resposta segura padrão
// ---------------------------------------------------------------------------

/**
 * Retornada sempre que qualquer guardrail ou validação de schema falhar.
 * Garante que o atendente nunca receba uma resposta potencialmente incorreta.
 *
 * `Object.freeze()` impede mutação em runtime: `const` protege a referência,
 * mas não o conteúdo do objeto. O freeze torna ambos imutáveis.
 */
export const SAFE_FALLBACK_RESPONSE: Readonly<ModelResponse> = Object.freeze({
  answer:
    "Não foi possível processar esta resposta. Por favor, consulte a documentação oficial ou entre em contato com o suporte.",
  source_document: "FALLBACK_SYSTEM",
  confidence_score: 0,
});

// ---------------------------------------------------------------------------
// Tipos internos
// ---------------------------------------------------------------------------

/** Resultado de cada verificação de guardrail. */
interface GuardrailResult {
  blocked: boolean;
  reason?: string;
}

/** Resultado final da validação completa. */
export interface ValidationResult {
  valid: boolean;
  response: ModelResponse;
  /** Motivo do bloqueio, quando `valid === false`. */
  blockReason?: string;
}

// ---------------------------------------------------------------------------
// Utilitários internos
// ---------------------------------------------------------------------------

/**
 * Normaliza texto para comparações determinísticas:
 *  - converte para minúsculas;
 *  - remove diacríticos via decomposição Unicode (NFD);
 *  - colapsa espaços múltiplos para facilitar matching de expressões regulares.
 *
 * Cobertura: acentos e cedilha do português brasileiro.
 * Fora do escopo: homoglifos, abreviações, siglas e variações com hífen.
 */
function normalizeText(text: string): string {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

// ---------------------------------------------------------------------------
// Guardrails
// ---------------------------------------------------------------------------

/**
 * Guardrail 1 — Source document obrigatório.
 *
 * Bloqueia qualquer resposta que não possua referência a um documento fonte.
 * Previne que o modelo "invente" respostas sem embasamento no corpus RAG.
 */
function checkSourceDocument(response: ModelResponse): GuardrailResult {
  const missing =
    !response.source_document || response.source_document.trim().length === 0;

  if (missing) {
    return {
      blocked: true,
      reason:
        "Guardrail 1 violado: 'source_document' ausente ou vazio. Resposta bloqueada por falta de grounding.",
    };
  }

  return { blocked: false };
}

/**
 * Guardrail 2 — Combinação proibida: carga perigosa + devolução permitida.
 *
 * Detecta respostas que simultaneamente:
 *  - mencionam contexto de carga perigosa, E
 *  - afirmam que a devolução é permitida / autorizada / aceita.
 *
 * Esse padrão representa um risco de compliance: o modelo pode interpretar
 * incorretamente a política interna e induzir o atendente ao erro.
 *
 * Estratégia de detecção:
 *  - Normalização Unicode (remoção de diacríticos) antes das comparações.
 *  - RegExp com \b (word boundary) para evitar falsos positivos por
 *    correspondência parcial de substrings.
 *  - Alternativas explícitas cobrindo variações lexicais previsíveis
 *    em português brasileiro.
 *
 * Limitação documentada: a detecção opera sobre tokens e não compreende
 * semântica de negação. A frase "a devolução não é permitida para carga
 * perigosa" contém os tokens monitorados e SERÁ bloqueada corretamente,
 * pois `mentionsReturnAllowed` exige padrões afirmativos (e.g. "pode
 * devolver", "devolucao permitida"). Negações explícitas como
 * "não pode devolver" não ativam `mentionsReturnAllowed` por design —
 * o regex ancora em verbos/adjetivos afirmativos sem prefixo de negação.
 * Paráfrases não mapeadas (ex.: "retorno liberado") continuam sendo
 * falsos negativos e devem ser adicionadas à lista conforme identificadas.
 */
function checkDangerousCargoReturn(response: ModelResponse): GuardrailResult {
  const normalized = normalizeText(response.answer);

  const DANGEROUS_CARGO_PATTERN =
    /\b(carga\s+perigosa|material\s+perigoso|produto\s+perigoso)\b/;

  /**
   * Padrões afirmativos de permissão de devolução.
   * Cada alternativa é delimitada por \b para evitar correspondências parciais.
   * "nao pode devolver" NÃO ativa este regex: o prefixo "nao" não faz parte
   * do padrão, e a sequência "pode devolver" só aparece isolada no texto
   * quando não há negação imediatamente anterior — limitação documentada acima.
   */
  const RETURN_ALLOWED_PATTERN =
    /\b(devolucao\s+(e|esta|foi|sera)\s+permitida|devolucao\s+permitida|devolucao\s+autorizada|pode\s+(ser\s+)?devolvido|pode\s+devolver|aceita?\s+devolucao|permite\s+devolucao|retorno\s+(e\s+)?(permitido|autorizado|aceito))\b/;

  const mentionsDangerousCargo = DANGEROUS_CARGO_PATTERN.test(normalized);
  const mentionsReturnAllowed = RETURN_ALLOWED_PATTERN.test(normalized);

  if (mentionsDangerousCargo && mentionsReturnAllowed) {
    return {
      blocked: true,
      reason:
        "Guardrail 2 violado: resposta afirma que devolução de carga perigosa é permitida. Bloqueada por risco de compliance.",
    };
  }

  return { blocked: false };
}

// ---------------------------------------------------------------------------
// Pipeline de guardrails
// ---------------------------------------------------------------------------

/**
 * Lista ordenada de guardrails.
 * A ordem importa: o primeiro bloqueio encerra o pipeline (fail-fast).
 */
const GUARDRAILS: ReadonlyArray<(r: ModelResponse) => GuardrailResult> = [
  checkSourceDocument,
  checkDangerousCargoReturn,
];

/**
 * Executa todos os guardrails sobre uma resposta já validada pelo schema.
 * Retorna o primeiro bloqueio encontrado, ou `{ blocked: false }` se passar em todos.
 */
function applyGuardrails(response: ModelResponse): GuardrailResult {
  for (const guardrail of GUARDRAILS) {
    const result = guardrail(response);
    if (result.blocked) {
      return result;
    }
  }
  return { blocked: false };
}

// ---------------------------------------------------------------------------
// Validação do schema
// ---------------------------------------------------------------------------

/**
 * Tenta fazer parse do input desconhecido contra o ModelResponseSchema.
 * Retorna `{ success: true, data }` ou `{ success: false, error }`.
 *
 * Separado da lógica de guardrails para manter responsabilidades isoladas.
 */
function parseModelOutput(
  raw: unknown
): { success: true; data: ModelResponse } | { success: false; error: string } {
  const result = ModelResponseSchema.safeParse(raw);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const messages = result.error.errors
    .map((e) => `[${e.path.join(".")}] ${e.message}`)
    .join("; ");

  return { success: false, error: messages };
}

// ---------------------------------------------------------------------------
// Ponto de entrada público
// ---------------------------------------------------------------------------

/**
 * Valida o output bruto do modelo e aplica todos os guardrails configurados.
 *
 * Fluxo:
 *  1. Parse + validação estrutural via Zod.
 *  2. Guardrail 1 — presença de source_document.
 *  3. Guardrail 2 — combinação proibida carga perigosa + devolução permitida.
 *
 * Em qualquer falha: loga o motivo e retorna SAFE_FALLBACK_RESPONSE.
 *
 * @param raw - Objeto bruto retornado pelo modelo (tipo desconhecido).
 * @returns ValidationResult com `valid`, `response` e opcionalmente `blockReason`.
 */
export function validateModelResponse(raw: unknown): ValidationResult {
  // --- Etapa 1: validação de schema ---
  const parsed = parseModelOutput(raw);

  if (!parsed.success) {
    logger.warn(
      { schemaError: parsed.error },
      "Falha na validação do schema Zod. Resposta bloqueada."
    );
    return {
      valid: false,
      response: SAFE_FALLBACK_RESPONSE,
      blockReason: `Schema inválido: ${parsed.error}`,
    };
  }

  const response = parsed.data;

  // --- Etapa 2: guardrails ---
  const guardrailResult = applyGuardrails(response);

  if (guardrailResult.blocked) {
    logger.warn(
      {
        blockReason: guardrailResult.reason,
        source_document: response.source_document,
        confidence_score: response.confidence_score,
      },
      "Resposta bloqueada por guardrail."
    );
    return {
      valid: false,
      response: SAFE_FALLBACK_RESPONSE,
      blockReason: guardrailResult.reason,
    };
  }

  // --- Resposta aprovada ---
  logger.info(
    {
      source_document: response.source_document,
      confidence_score: response.confidence_score,
    },
    "Resposta validada com sucesso."
  );

  return { valid: true, response };
}