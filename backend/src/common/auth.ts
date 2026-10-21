import {
  CanActivate,
  ExecutionContext,
  ForbiddenException,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import type { Request } from 'express';
import jwt from 'jsonwebtoken';
import { required } from './config.js';
export type Actor = { id: string; email: string; name: string; role: 'CLIENT' | 'PROVIDER' };
export type AuthRequest = Request & { actor: Actor };
export function signActor(actor: Actor): string {
  return jwt.sign(actor, required('JWT_SECRET'), {
    algorithm: 'HS256',
    issuer: 'marketplace',
    audience: 'marketplace',
    subject: actor.email,
    expiresIn: '1h',
  });
}
export function verifyActor(token: string): Actor {
  try {
    const value = jwt.verify(token, required('JWT_SECRET'), {
      algorithms: ['HS256'],
      issuer: 'marketplace',
      audience: 'marketplace',
    });
    if (
      typeof value === 'string' ||
      typeof value.email !== 'string' ||
      value.sub !== value.email ||
      typeof value.name !== 'string' ||
      value.id !== value.email ||
      !['CLIENT', 'PROVIDER'].includes(value.role)
    )
      throw new Error('Invalid principal');
    return { id: value.id, email: value.email, name: value.name, role: value.role };
  } catch {
    throw new UnauthorizedException('Invalid or expired bearer token');
  }
}
@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest<AuthRequest>();
    const authorization = request.headers.authorization;
    if (!authorization?.startsWith('Bearer '))
      throw new UnauthorizedException('Bearer token required');
    request.actor = verifyActor(authorization.slice(7));
    return true;
  }
}
export function requireRole(actor: Actor, role: Actor['role']): void {
  if (actor.role !== role)
    throw new ForbiddenException(`Only ${role.toLowerCase()} accounts may perform this action`);
}
