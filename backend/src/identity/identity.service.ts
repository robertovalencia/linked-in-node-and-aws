import { Injectable, OnApplicationBootstrap, UnauthorizedException } from '@nestjs/common';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { Database } from '../common/database.js';
import { Actor, signActor } from '../common/auth.js';
import { hashPassword, verifyPassword } from './password.js';
@Injectable()
export class IdentityService implements OnApplicationBootstrap {
  private dummyHash = '';
  constructor(private readonly db: Database) {}
  async onApplicationBootstrap(): Promise<void> {
    this.dummyHash = await hashPassword('dummy-password-never-used');
    if (process.env.SEED_DEMO !== 'true') return;
    const providers: { ownerEmail: string; name: string }[] = JSON.parse(
      await readFile(join(process.cwd(), 'seeds/providers.json'), 'utf8'),
    );
    const accounts: Actor[] = [
      ...providers.map((p) => ({
        id: p.ownerEmail,
        email: p.ownerEmail,
        name: p.name,
        role: 'PROVIDER' as const,
      })),
      {
        id: 'company@demo.local',
        email: 'company@demo.local',
        name: 'Morgan at Acme',
        role: 'CLIENT',
      },
      {
        id: 'individual@demo.local',
        email: 'individual@demo.local',
        name: 'Jordan Ellis',
        role: 'CLIENT',
      },
    ];
    const passwordHash = await hashPassword('DemoPass123!');
    await this.db.transaction(async (client) => {
      for (const actor of accounts)
        await client.query(
          'INSERT INTO accounts(email,name,role,password_hash) VALUES($1,$2,$3,$4) ON CONFLICT(email) DO NOTHING',
          [actor.email, actor.name, actor.role, passwordHash],
        );
    });
  }
  async login(email: string, password: string) {
    const result = await this.db.query(
      'SELECT email,name,role,password_hash FROM accounts WHERE email=$1',
      [email.toLowerCase()],
    );
    const account = result.rows[0];
    const valid = await verifyPassword(password, account?.password_hash ?? this.dummyHash);
    if (!account || !valid) throw new UnauthorizedException('Invalid email or password');
    const actor: Actor = {
      id: account.email,
      email: account.email,
      name: account.name,
      role: account.role,
    };
    return { token: signActor(actor), ...actor };
  }
}
