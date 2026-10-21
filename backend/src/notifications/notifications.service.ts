import { ForbiddenException, Injectable, NotFoundException } from '@nestjs/common';
import { randomUUID } from 'node:crypto';
import { z } from 'zod';
import { Actor } from '../common/auth.js';
import { Database } from '../common/database.js';
import { eventSchema } from '../inquiries/inquiry.schema.js';
type NotificationRow = {
  id: string;
  inquiry_id: string;
  message: string;
  created_at: Date | string;
  read: boolean;
};
export function notificationView(row: NotificationRow) {
  return {
    id: row.id,
    inquiryId: row.inquiry_id,
    message: row.message,
    createdAt: new Date(row.created_at).toISOString(),
    read: row.read,
  };
}
@Injectable()
export class NotificationsService {
  constructor(private readonly db: Database) {}
  async consume(payload: unknown): Promise<void> {
    const event = eventSchema.parse(payload);
    // A single statement commits receipt and inbox data; duplicate delivery becomes a no-op.
    await this.db.query(
      'INSERT INTO notifications(id,event_id,inquiry_id,recipient_email,message,created_at) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT(event_id) DO NOTHING',
      [
        randomUUID(),
        event.eventId,
        event.inquiryId,
        event.recipientEmail,
        `${event.clientName} sent a new inquiry: ${event.subject}`,
        event.createdAt,
      ],
    );
  }
  async list(actor: Actor) {
    const result = await this.db.query<NotificationRow>(
      'SELECT * FROM notifications WHERE recipient_email=$1 ORDER BY created_at DESC,id',
      [actor.email],
    );
    return result.rows.map(notificationView);
  }
  async read(actor: Actor, id: string) {
    z.uuid().parse(id);
    return this.db.transaction(async (client) => {
      const result = await client.query('SELECT * FROM notifications WHERE id=$1 FOR UPDATE', [id]);
      const row = result.rows[0];
      if (!row) throw new NotFoundException('Notification not found');
      if (row.recipient_email !== actor.email)
        throw new ForbiddenException('Notification belongs to another account');
      const updated = await client.query(
        'UPDATE notifications SET read=true WHERE id=$1 RETURNING *',
        [id],
      );
      return notificationView(updated.rows[0]);
    });
  }
}
