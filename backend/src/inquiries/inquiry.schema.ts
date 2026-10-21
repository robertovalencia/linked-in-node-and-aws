import { z } from 'zod';
export const inquirySchema = z
  .object({
    providerId: z.string().regex(/^[a-z0-9-]{2,80}$/),
    subject: z.string().trim().min(5).max(160),
    message: z.string().trim().min(20).max(5000),
    budget: z
      .number()
      .min(1)
      .max(9999999999.99)
      .refine(
        (value) => Math.abs(value * 100 - Math.round(value * 100)) < 0.0001,
        'At most two decimal places',
      ),
    clientType: z.enum(['COMPANY', 'INDIVIDUAL']),
  })
  .strict();
export type CreateInquiry = z.infer<typeof inquirySchema>;
export const statusSchema = z.object({ status: z.enum(['ACCEPTED', 'DECLINED']) }).strict();
export const eventSchema = z
  .object({
    eventId: z.uuid(),
    inquiryId: z.uuid(),
    recipientEmail: z.email(),
    providerName: z.string().min(1).max(100),
    clientName: z.string().min(1).max(100),
    subject: z.string().min(1).max(160),
    createdAt: z.iso.datetime(),
  })
  .strict();
