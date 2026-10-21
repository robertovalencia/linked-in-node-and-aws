import 'reflect-metadata';
import { Module, Type } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import helmet from 'helmet';
import { json } from 'express';
import { validateConfig, serviceName, SERVICES } from './common/config.js';
import { Database } from './common/database.js';
import { AuthGuard } from './common/auth.js';
import { ErrorFilter } from './common/errors.js';
import { HealthController, WorkerHealth } from './common/health.js';
import { OutboxPublisher, InquiryConsumer } from './common/messaging.js';
import { IdentityController } from './identity/identity.controller.js';
import { IdentityService } from './identity/identity.service.js';
import { CatalogController } from './catalog/catalog.controller.js';
import { CatalogService } from './catalog/catalog.service.js';
import { InquiriesController } from './inquiries/inquiries.controller.js';
import { InquiriesService } from './inquiries/inquiries.service.js';
import { NotificationsController } from './notifications/notifications.controller.js';
import { NotificationsService } from './notifications/notifications.service.js';

async function bootstrap(): Promise<void> {
  validateConfig();
  const service = serviceName();
  const controllers: Record<string, Type> = {
    identity: IdentityController,
    catalog: CatalogController,
    inquiries: InquiriesController,
    notifications: NotificationsController,
  };
  const providers: Record<string, Type[]> = {
    identity: [IdentityService],
    catalog: [CatalogService],
    inquiries: [InquiriesService, OutboxPublisher],
    notifications: [NotificationsService, InquiryConsumer],
  };
  @Module({
    controllers: [HealthController, controllers[service]],
    providers: [Database, AuthGuard, WorkerHealth, ...providers[service]],
  })
  class ApplicationModule {}
  const app = await NestFactory.create(ApplicationModule, {
    bodyParser: false,
    logger: ['log', 'warn', 'error'],
  });
  app.use(helmet());
  app.use(json({ limit: '128kb' }));
  app.useGlobalFilters(new ErrorFilter());
  app.enableShutdownHooks();
  const port = Number(process.env.PORT ?? 8181 + SERVICES.indexOf(service));
  if (!Number.isInteger(port) || port < 1 || port > 65535)
    throw new Error('PORT must be a valid TCP port');
  await app.listen(port, '0.0.0.0');
}
void bootstrap().catch((error) => {
  console.error(error instanceof Error ? error.stack : error);
  process.exitCode = 1;
});
