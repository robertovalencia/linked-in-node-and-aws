import { pathToFileURL } from 'node:url';
import { Database } from '../common/database.js';
import { serviceName } from '../common/config.js';

export async function replayPublishedOutbox(database?: Database): Promise<number> {
  if (serviceName() !== 'inquiries')
    throw new Error('Outbox replay requires the inquiries capability');
  if (process.env.REPLAY_OUTBOX_CONFIRM !== 'replay-all-published-events')
    throw new Error('Explicit REPLAY_OUTBOX_CONFIRM is required');
  const db = database ?? new Database();
  try {
    // Preserve original event IDs and payloads. Notification uniqueness makes repeats harmless.
    const result = await db.query<{ replay_count: string }>(
      'WITH replay AS (UPDATE outbox SET published_at=NULL WHERE published_at IS NOT NULL RETURNING event_id) SELECT count(*) AS replay_count FROM replay',
    );
    return Number(result.rows[0].replay_count);
  } finally {
    if (!database) await db.onModuleDestroy();
  }
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  void replayPublishedOutbox()
    .then((count) => console.log(JSON.stringify({ event: 'outbox_replay_queued', count })))
    .catch(() => {
      console.error(
        'Outbox replay failed; check confirmation, capability and owned database connectivity',
      );
      process.exitCode = 1;
    });
}
