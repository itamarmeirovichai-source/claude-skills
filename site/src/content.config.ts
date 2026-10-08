import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

const films = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/films' }),
  schema: z.object({
    order: z.number(),
    idea: z.string(),
    status: z.enum(['final', 'placeholder']),
    tools: z.array(z.string()).default([]),
  }),
});

const faq = defineCollection({
  loader: file('./src/content/faq.json'),
  schema: z.object({ q: z.string(), a: z.string(), order: z.number() }),
});

export const collections = { films, faq };
