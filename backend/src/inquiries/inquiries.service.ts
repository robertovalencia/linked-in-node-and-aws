import {
  BadRequestException,
  ConflictException,
  ForbiddenException,
  Injectable,
  NotFoundException,
  ServiceUnavailableException,
} from '@nestjs/common';
import { createHash, randomUUID } from 'node:crypto';
import { z } from 'zod';
import { Actor, requireRole } from '../common/auth.js';
import { Database } from '../common/database.js';
import { required } from '../common/config.js';
import { inquirySchema, statusSchema, CreateInquiry } from './inquiry.schema.js';
export function fingerprint(input: CreateInquiry): string {
  return createHash('sha256')
    .update(
      JSON.stringify([
        input.providerId,
        input.subject,
        input.message,
        input.budget,
        input.clientType,
      ]),
    )
    .digest('hex');
}
type InquiryRow = {
  id: string;
  provider_id: string;
  provider_name: string;
  client_name: string;
  subject: string;
  message: string;
  budget: string | number;
  client_type: string;
  status: string;
  created_at: Date | string;
};
export function inquiryView(row: InquiryRow) {
  return {
    id: row.id,
    providerId: row.provider_id,
    providerName: row.provider_name,
    clientName: row.client_name,
    subject: row.subject,
    message: row.message,
    budget: Number(row.budget),
    clientType: row.client_type,
    status: row.status,
    createdAt: new Date(row.created_at).toISOString(),
  };
}
@Injectable()
export class InquiriesService {
  constructor(private readonly db: Database) {}
  private async provider(id: string) {
    let response: Response;
    try {
      response = await fetch(
        `${required('CATALOG_URL').replace(/\/$/, '')}/internal/providers/${encodeURIComponent(id)}`,
        {
          headers: { 'X-Internal-Key': required('INTERNAL_API_KEY') },
          signal: AbortSignal.timeout(5000),
        },
      );
    } catch {
      throw new ServiceUnavailableException(
        'Catalog is unavailable; retry with the same idempotency key',
      );
    }
    if (response.status === 404) throw new NotFoundException('Provider not found');
    if (!response.ok) throw new ServiceUnavailableException('Catalog lookup failed');
    try {
      return z
        .object({ id: z.string(), ownerEmail: z.email(), name: z.string() })
        .parse(await response.json());
    } catch {
      throw new ServiceUnavailableException('Catalog returned an invalid provider');
    }
  }
  async create(actor: Actor, key: string | undefined, body: unknown) {
    requireRole(actor, 'CLIENT');
    if (!key || !/^[A-Za-z0-9_-]{8,100}$/.test(key))
      throw new BadRequestException(
        'Idempotency-Key requires 8–100 letters, digits, underscores or hyphens',
      );
    const input = inquirySchema.parse(body);
    const hash = fingerprint(input);
    return this.db.transaction(async (client) => {
      // The transaction-scoped lock serializes the same client/key across every replica.
      await client.query('SELECT pg_advisory_xact_lock(hashtextextended($1,0))', [
        JSON.stringify([actor.email, key]),
      ]);
      const previous = await client.query(
        'SELECT * FROM inquiries WHERE client_email=$1 AND idempotency_key=$2',
        [actor.email, key],
      );
      if (previous.rows[0]) {
        if (previous.rows[0].request_hash !== hash)
          throw new ConflictException('Idempotency key already used for a different inquiry');
        return inquiryView(previous.rows[0]);
      }
      const target = await this.provider(input.providerId);
      const id = randomUUID();
      const eventId = randomUUID();
      const createdAt = new Date().toISOString();
      const inserted = await client.query(
        'INSERT INTO inquiries(id,provider_id,provider_email,provider_name,client_email,client_name,subject,message,budget,client_type,created_at,idempotency_key,request_hash) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13) RETURNING *',
        [
          id,
          target.id,
          target.ownerEmail,
          target.name,
          actor.email,
          actor.name,
          input.subject,
          input.message,
          input.budget,
          input.clientType,
          createdAt,
          key,
          hash,
        ],
      );
      const event = {
        eventId,
        inquiryId: id,
        recipientEmail: target.ownerEmail,
        providerName: target.name,
        clientName: actor.name,
        subject: input.subject,
        createdAt,
      };
      await client.query('INSERT INTO outbox(event_id,inquiry_id,payload) VALUES($1,$2,$3)', [
        eventId,
        id,
        event,
      ]);
      return inquiryView(inserted.rows[0]);
    });
  }
  async list(actor: Actor) {
    const result = await this.db.query<InquiryRow>(
      'SELECT * FROM inquiries WHERE client_email=$1 OR provider_email=$1 ORDER BY created_at DESC,id',
      [actor.email],
    );
    return result.rows.map(inquiryView);
  }
  async respond(actor: Actor, id: string, body: unknown) {
    requireRole(actor, 'PROVIDER');
    const input = statusSchema.parse(body);
    z.uuid().parse(id);
    return this.db.transaction(async (client) => {
      const result = await client.query('SELECT * FROM inquiries WHERE id=$1 FOR UPDATE', [id]);
      const row = result.rows[0];
      if (!row) throw new NotFoundException('Inquiry not found');
      if (row.provider_email !== actor.email)
        throw new ForbiddenException('Inquiry belongs to another provider');
      if (row.status !== 'PENDING' && row.status !== input.status)
        throw new ConflictException('Inquiry already resolved');
      const updated = await client.query('UPDATE inquiries SET status=$1 WHERE id=$2 RETURNING *', [
        input.status,
        id,
      ]);
      return inquiryView(updated.rows[0]);
    });
  }
}
