import { z } from 'zod';
const text = (length: number) => z.string().trim().min(1).max(length);
const secureUrl = z
  .string()
  .max(2048)
  .url()
  .refine((v) => v.startsWith('https://'), 'HTTPS URL required');
export const providerSchema = z
  .object({
    id: z.string().regex(/^[a-z0-9-]{2,80}$/),
    name: text(100),
    headline: text(180),
    location: text(120),
    category: z.enum(['Software Development', 'IT Consulting', 'Design', 'Marketing']),
    about: text(5000),
    avatarUrl: z
      .string()
      .max(2048)
      .regex(/^(https:\/\/[^\s]+|\/(?!\/)[^\s]+)$/),
    coverColor: z.string().regex(/^#[0-9a-fA-F]{6}$/),
    skills: z.array(text(60)).min(1).max(30),
    tools: z.array(text(60)).min(1).max(30),
    services: z.array(text(180)).min(1).max(15),
    experience: z
      .array(
        z
          .object({
            title: text(120),
            company: text(120),
            period: text(80),
            description: text(1500),
          })
          .strict(),
      )
      .max(20),
    portfolio: z
      .array(z.object({ title: text(120), description: text(1500), url: secureUrl }).strict())
      .max(12),
    hourlyRate: z.number().int().min(5).max(1000),
    currency: z.literal('USD'),
    available: z.boolean(),
    rating: z.number().min(0).max(5),
    reviewCount: z.number().int().nonnegative(),
    completedProjects: z.number().int().nonnegative(),
    responseTime: text(80),
  })
  .strict();
export type Provider = z.infer<typeof providerSchema>;
export const searchSchema = z
  .object({
    q: z.string().max(200).optional(),
    category: z.string().max(80).optional(),
    skill: z.string().max(60).optional(),
    maxRate: z.coerce.number().int().min(0).max(1e6).optional(),
    available: z
      .enum(['true', 'false'])
      .transform((v) => v === 'true')
      .optional(),
    sort: z.enum(['recommended', 'rate-asc', 'rating']).default('recommended'),
    page: z.coerce.number().int().min(0).max(1e6).default(0),
    size: z.coerce.number().int().min(1).max(50).default(12),
  })
  .strict();
