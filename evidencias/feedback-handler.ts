import { app, HttpRequest, HttpResponseInit } from '@azure/functions';
import { CosmosClient } from '@azure/cosmos';
import pino from 'pino';
import { z } from 'zod';

const logger = pino({ name: 'feedback-handler' });

const connectionString = process.env.COSMOS_CONNECTION_STRING;

if (!connectionString) {
  throw new Error(
    'Variável de ambiente COSMOS_CONNECTION_STRING não está configurada.'
  );
}

const cosmosClient = new CosmosClient(connectionString);
const container = cosmosClient.database('novatech').container('feedbacks');

const FeedbackSchema = z.object({
  queryId: z.string().uuid(),
  rating: z.number().int().min(1).max(5),
  comment: z.string().trim().max(2000).optional(),
  attendantEmail: z.string().email(),
});

type FeedbackInput = z.infer<typeof FeedbackSchema>;

function mapValidationErrors(error: z.ZodError) {
  return error.issues.map((issue) => ({
    path: issue.path.join('.'),
    message: issue.message,
  }));
}

function getErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : 'Erro desconhecido';
}

export async function feedbackHandler(
  request: HttpRequest
): Promise<HttpResponseInit> {
  const rawBody = await request.json();

  const parseResult = FeedbackSchema.safeParse(rawBody);

  if (!parseResult.success) {
    const validationErrors = mapValidationErrors(parseResult.error);

    logger.warn(
      { issues: validationErrors },
      'Payload de feedback inválido'
    );

    return {
      status: 400,
      jsonBody: {
        message: 'Payload inválido.',
        errors: validationErrors,
      },
    };
  }

  const input: FeedbackInput = parseResult.data;

  const feedback = {
    queryId: input.queryId,
    rating: input.rating,
    comment: input.comment,
    attendantEmail: input.attendantEmail,
    timestamp: new Date().toISOString(),
  };

  try {
    await container.items.create(feedback);

    logger.info(
      { queryId: feedback.queryId, rating: feedback.rating },
      'Feedback registrado com sucesso'
    );

    return {
      status: 201,
      jsonBody: {
        queryId: feedback.queryId,
        timestamp: feedback.timestamp,
      },
    };
  } catch (error) {
    logger.error(
      {
        queryId: feedback.queryId,
        errorMessage: getErrorMessage(error),
      },
      'Falha ao persistir feedback no Cosmos DB'
    );

    return {
      status: 500,
      jsonBody: {
        message: 'Erro interno. Não foi possível registrar o feedback.',
      },
    };
  }
}

app.http('feedback', {
  methods: ['POST'],
  handler: feedbackHandler,
});