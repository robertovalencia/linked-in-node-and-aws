import { Body, Controller, Get, Headers, Param, Patch, Post, Req, UseGuards } from '@nestjs/common';
import { AuthGuard, AuthRequest } from '../common/auth.js';
import { InquiriesService } from './inquiries.service.js';
@Controller('api/inquiries')
@UseGuards(AuthGuard)
export class InquiriesController {
  constructor(private readonly inquiries: InquiriesService) {}
  @Post() create(
    @Req() request: AuthRequest,
    @Headers('idempotency-key') key: string | undefined,
    @Body() body: unknown,
  ) {
    return this.inquiries.create(request.actor, key, body);
  }
  @Get() list(@Req() request: AuthRequest) {
    return this.inquiries.list(request.actor);
  }
  @Patch(':id/status') respond(
    @Req() request: AuthRequest,
    @Param('id') id: string,
    @Body() body: unknown,
  ) {
    return this.inquiries.respond(request.actor, id, body);
  }
}
