import mongoose from 'mongoose'

const feedbackSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  paper: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Paper',
    required: true
  },
  rating: {
    type: Number,
    min: 1,
    max: 5,
    required: true
  },
  comment: {
    type: String,
    trim: true
  },
  helpful: {
    type: Boolean,
    default: false
  }
}, {
  timestamps: true
})

export const Feedback = mongoose.model('Feedback', feedbackSchema)

