import { ArgumentsHost, Catch, ExceptionFilter, HttpException, Logger } from '@nestjs/common';
import { ZodError } from 'zod';
import type { Response } from 'express';
@Catch()
export class ErrorFilter implements ExceptionFilter {
  private readonly logger = new Logger('HttpErrors');
  catch(error: unknown, host: ArgumentsHost): void {
    const response = host.switchToHttp().getResponse<Response>();
    const parserStatus =
      typeof error === 'object' &&
      error !== null &&
      'status' in error &&
      [400, 413].includes(Number(error.status))
        ? Number(error.status)
        : undefined;
    const status =
      error instanceof ZodError
        ? 400
        : error instanceof HttpException
          ? error.getStatus()
          : (parserStatus ?? 500);
    let detail =
      status === 500
        ? 'Internal server error'
        : error instanceof ZodError
          ? error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('; ')
          : (error as Error).message;
    if (status === 500) this.logger.error(error instanceof Error ? error.stack : String(error));
    if (detail.length > 1500) detail = detail.slice(0, 1500);
    response.status(status).json({ status, detail });
  }
}
