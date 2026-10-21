import {
  Body,
  Controller,
  Get,
  HttpCode,
  HttpException,
  Post,
  Req,
  UseGuards,
} from '@nestjs/common';
import type { Request } from 'express';
import { z } from 'zod';
import { AuthGuard, AuthRequest } from '../common/auth.js';
import { IdentityService } from './identity.service.js';
const loginSchema = z
  .object({ email: z.email().max(254), password: z.string().min(1).max(200) })
  .strict();
@Controller('api/auth')
export class IdentityController {
  // Per-process throttle protects password hashing; the private AWS dev environment has no additional ingress rate rule.
  private readonly attempts = new Map<string, { count: number; until: number }>();
  constructor(private readonly identity: IdentityService) {}
  @Post('login') @HttpCode(200) async login(@Body() body: unknown, @Req() request: Request) {
    const now = Date.now();
    for (const [key, value] of this.attempts) if (value.until <= now) this.attempts.delete(key);
    const key = request.ip ?? 'unknown';
    const attempts = this.attempts.get(key) ?? { count: 0, until: now + 60_000 };
    if (++attempts.count > 30)
      throw new HttpException('Too many login attempts; retry in one minute', 429);
    this.attempts.set(key, attempts);
    const input = loginSchema.parse(body);
    return this.identity.login(input.email, input.password);
  }
  @Get('me') @UseGuards(AuthGuard) me(@Req() request: AuthRequest) {
    return request.actor;
  }
}
