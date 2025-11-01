import mongoose from 'mongoose'

const paperSchema = new mongoose.Schema({
  title: {
    type: String,
    required: [true, 'Please add a title'],
    trim: true
  },
  abstract: {
    type: String,
    trim: true
  },
  authors: [{
    type: String,
    trim: true
  }],
  keywords: [{
    type: String,
    trim: true
  }],
  publicationDate: {
    type: Date,
    default: Date.now
  },
  url: {
    type: String,
    trim: true
  },
  citations: {
    type: Number,
    default: 0,
    min: 0
  },
  relevanceScore: {
    type: Number,
    min: 0,
    max: 100
  },
  summary: {
    type: String
  },
  metadata: {
    type: mongoose.Schema.Types.Mixed
  }
}, {
  timestamps: true
})

// Index for search
paperSchema.index({ title: 'text', abstract: 'text', keywords: 'text' })

export const Paper = mongoose.model('Paper', paperSchema)

