import mongoose from 'mongoose'
import { logger } from '../utils/logger.js'

export const connectDB = async () => {
  // Check if MONGO_URI or MONGODB_URI is provided
  const mongoUri = process.env.MONGO_URI || process.env.MONGODB_URI
  
  if (!mongoUri) {
    logger.info('Mongo URI not provided, skipping Mongo connection')
    return
  }

  try {
    const conn = await mongoose.connect(mongoUri, {
      // MongoDB connection options
    })

    logger.info(`MongoDB Connected: ${conn.connection.host}`)
  } catch (error) {
    logger.error(`MongoDB connection error: ${error.message}`)
    // Don't exit the process - let the HTTP server keep running
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

