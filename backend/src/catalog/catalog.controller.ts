import {
  Body,
  Controller,
  ForbiddenException,
  Get,
  Headers,
  Param,
  Put,
  Query,
  Req,
  UseGuards,
} from '@nestjs/common';
import { timingSafeEqual } from 'node:crypto';
import { AuthGuard, AuthRequest, requireRole } from '../common/auth.js';
import { required } from '../common/config.js';
import { CatalogService } from './catalog.service.js';
@Controller()
export class CatalogController {
  constructor(private readonly catalog: CatalogService) {}
  @Get('api/providers') search(@Query() query: unknown) {
    return this.catalog.search(query);
  }
  @Get('api/providers/me') @UseGuards(AuthGuard) mine(@Req() request: AuthRequest) {
    requireRole(request.actor, 'PROVIDER');
    return this.catalog.mine(request.actor.email);
  }
  @Put('api/providers/me') @UseGuards(AuthGuard) update(
    @Req() request: AuthRequest,
    @Body() input: unknown,
  ) {
    requireRole(request.actor, 'PROVIDER');
    return this.catalog.update(request.actor.email, input);
  }
  @Get('api/providers/:id') get(@Param('id') id: string) {
    return this.catalog.get(id);
  }
  @Get('internal/providers/:id') async internal(
    @Param('id') id: string,
    @Headers('x-internal-key') key?: string,
  ) {
    const expected = Buffer.from(required('INTERNAL_API_KEY'));
    const received = Buffer.from(key ?? '');
    if (received.length !== expected.length || !timingSafeEqual(received, expected))
      throw new ForbiddenException('Internal service key required');
    const row = await this.catalog.row(id);
    return { id: row.id, ownerEmail: row.owner_email, name: row.document.name };
  }
}
