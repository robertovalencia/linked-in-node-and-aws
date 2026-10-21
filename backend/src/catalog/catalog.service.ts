import {
  ForbiddenException,
  Injectable,
  NotFoundException,
  OnApplicationBootstrap,
} from '@nestjs/common';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { Database } from '../common/database.js';
import { Provider, providerSchema, searchSchema } from './provider.schema.js';
@Injectable()
export class CatalogService implements OnApplicationBootstrap {
  constructor(private readonly db: Database) {}
  async onApplicationBootstrap(): Promise<void> {
    if (process.env.SEED_DEMO !== 'true') return;
    const providers: (Provider & { ownerEmail: string })[] = JSON.parse(
      await readFile(join(process.cwd(), 'seeds/providers.json'), 'utf8'),
    );
    await this.db.transaction(async (client) => {
      for (const entry of providers) {
        const { ownerEmail, ...document } = entry;
        providerSchema.parse(document);
        await client.query(
          'INSERT INTO providers(id,owner_email,document) VALUES($1,$2,$3) ON CONFLICT(id) DO NOTHING',
          [document.id, ownerEmail, document],
        );
      }
    });
  }
  async row(id: string) {
    const result = await this.db.query(
      'SELECT id,owner_email,document FROM providers WHERE id=$1',
      [id],
    );
    if (!result.rows[0]) throw new NotFoundException('Provider not found');
    return result.rows[0];
  }
  async get(id: string): Promise<Provider> {
    return (await this.row(id)).document;
  }
  async mine(email: string): Promise<Provider> {
    const result = await this.db.query('SELECT document FROM providers WHERE owner_email=$1', [
      email,
    ]);
    if (!result.rows[0]) throw new NotFoundException('Provider profile not found');
    return result.rows[0].document;
  }
  async update(email: string, input: unknown): Promise<Provider> {
    const updated = providerSchema.parse(input);
    return this.db.transaction(async (client) => {
      const result = await client.query(
        'SELECT id,document FROM providers WHERE owner_email=$1 FOR UPDATE',
        [email],
      );
      const row = result.rows[0];
      if (!row) throw new NotFoundException('Provider profile not found');
      if (row.id !== updated.id)
        throw new ForbiddenException('Cannot edit another provider profile');
      const document = {
        ...updated,
        rating: row.document.rating,
        reviewCount: row.document.reviewCount,
        completedProjects: row.document.completedProjects,
      };
      await client.query('UPDATE providers SET document=$1 WHERE id=$2', [document, row.id]);
      return document;
    });
  }
  async search(input: unknown) {
    const query = searchSchema.parse(input);
    // Parameterized JSONB predicates keep filtering/pagination in PostgreSQL as the catalog grows.
    const values: unknown[] = [];
    const where: string[] = [];
    const add = (value: unknown) => {
      values.push(value);
      return `$${values.length}`;
    };
    if (query.q?.trim()) {
      const escaped = query.q.trim().replace(/[\\%_]/g, '\\$&');
      where.push(
        `(concat_ws(' ', document->>'name',document->>'headline',document->>'about',document->>'skills',document->>'tools',document->>'services',document->>'location')) ILIKE ${add(`%${escaped}%`)}`,
      );
    }
    if (query.category) where.push(`lower(document->>'category')=lower(${add(query.category)})`);
    if (query.skill)
      where.push(
        `EXISTS (SELECT 1 FROM jsonb_array_elements_text(document->'skills') skill WHERE lower(skill)=lower(${add(query.skill)}))`,
      );
    if (query.maxRate !== undefined)
      where.push(`(document->>'hourlyRate')::numeric<=${add(query.maxRate)}`);
    if (query.available !== undefined)
      where.push(`(document->>'available')::boolean=${add(query.available)}`);
    const condition = where.length ? `WHERE ${where.join(' AND ')}` : '';
    const order =
      query.sort === 'rate-asc'
        ? "(document->>'hourlyRate')::numeric ASC,id ASC"
        : "(document->>'rating')::numeric DESC,id ASC";
    const result = await this.db.query(
      `WITH filtered AS (SELECT id,document FROM providers ${condition}) SELECT (SELECT count(*)::int FROM filtered) AS total, COALESCE((SELECT jsonb_agg(page.document ORDER BY page.ordinal) FROM (SELECT document,row_number() OVER (ORDER BY ${order}) ordinal FROM filtered ORDER BY ${order} LIMIT ${add(query.size)} OFFSET ${add(query.page * query.size)}) page),'[]'::jsonb) AS items`,
      values,
    );
    return result.rows[0];
  }
}
