import Joi from 'joi'

export const createPaperSchema = Joi.object({
  title: Joi.string().required(),
  abstract: Joi.string().optional(),
  authors: Joi.array().items(Joi.string()).optional(),
  keywords: Joi.array().items(Joi.string()).optional(),
  publicationDate: Joi.date().optional(),
  url: Joi.string().uri().optional(),
  citations: Joi.number().min(0).optional()
})

export const updatePaperSchema = Joi.object({
  title: Joi.string().optional(),
  abstract: Joi.string().optional(),
  authors: Joi.array().items(Joi.string()).optional(),
  keywords: Joi.array().items(Joi.string()).optional(),
  publicationDate: Joi.date().optional(),
  url: Joi.string().uri().optional(),
  citations: Joi.number().min(0).optional()
})

