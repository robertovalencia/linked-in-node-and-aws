import { Controller, Get, Param, Patch, Req, UseGuards } from '@nestjs/common';
import { AuthGuard, AuthRequest } from '../common/auth.js';
import { NotificationsService } from './notifications.service.js';
@Controller('api/notifications')
@UseGuards(AuthGuard)
export class NotificationsController {
  constructor(private readonly notifications: NotificationsService) {}
  @Get() list(@Req() request: AuthRequest) {
    return this.notifications.list(request.actor);
  }
  @Patch(':id/read') read(@Req() request: AuthRequest, @Param('id') id: string) {
    return this.notifications.read(request.actor, id);
  }
}
