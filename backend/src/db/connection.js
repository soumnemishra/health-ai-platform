import mongoose from 'mongoose'
import { logger } from '../utils/logger.js'

export const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/health_ai', {
      // MongoDB connection options
    })

    logger.info(`MongoDB Connected: ${conn.connection.host}`)
  } catch (error) {
    logger.error(`MongoDB connection error: ${error.message}`)
    process.exit(1)
  }
}

// Handle connection events
mongoose.connection.on('disconnected', () => {
  logger.warn('MongoDB disconnected')
})

mongoose.connection.on('error', (err) => {
  logger.error(`MongoDB connection error: ${err.message}`)
})

export default mongoose

