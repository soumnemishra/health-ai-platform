import cron from 'node-cron'
import { logger } from '../utils/logger.js'
import { Alert } from '../models/Alert.model.js'

/**
 * Cleanup job - runs every week
 * Removes old alerts and cleans up expired data
 */
export function setupCleanupJob() {
  cron.schedule('0 0 * * 0', async () => {
    logger.info('Running cleanup job...')
    
    try {
      // Delete read alerts older than 30 days
      const thirtyDaysAgo = new Date()
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

      const result = await Alert.deleteMany({
        read: true,
        createdAt: { $lt: thirtyDaysAgo }
      })

      logger.info(`Cleanup job: Deleted ${result.deletedCount} old alerts`)
      logger.info('Cleanup job completed successfully')
    } catch (error) {
      logger.error(`Cleanup job error: ${error.message}`)
    }
  })

  logger.info('Cleanup job scheduled (runs weekly on Sundays)')
}

