import dotenv from 'dotenv'
import app from './app.js'
import { logger } from './utils/logger.js'
import { setupDailyDigestJob } from './jobs/dailyDigest.job.js'
import { setupCleanupJob } from './jobs/cleanup.job.js'

// Load environment variables
dotenv.config()

// Setup scheduled jobs
setupDailyDigestJob()
setupCleanupJob()

const PORT = process.env.PORT || 3000
const NODE_ENV = process.env.NODE_ENV || 'development'

// Start server
const server = app.listen(PORT, () => {
  logger.info(`Server running in ${NODE_ENV} mode on port ${PORT}`)
})

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  logger.error(`Unhandled Rejection: ${err.message}`)
  server.close(() => {
    process.exit(1)
  })
})

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
  logger.error(`Uncaught Exception: ${err.message}`)
  process.exit(1)
})

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down gracefully...')
  server.close(() => {
    logger.info('Process terminated')
  })
})

