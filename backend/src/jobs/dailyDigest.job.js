import cron from 'node-cron'
import { logger } from '../utils/logger.js'

/**
 * Daily digest job - runs every day at 9 AM
 * Sends daily summaries to users
 */
export function setupDailyDigestJob() {
  cron.schedule('0 9 * * *', async () => {
    logger.info('Running daily digest job...')
    
    try {
      // TODO: Implement daily digest logic
      // 1. Get all active users
      // 2. Generate personalized digests
      // 3. Send notifications/alerts
      
      logger.info('Daily digest job completed successfully')
    } catch (error) {
      logger.error(`Daily digest job error: ${error.message}`)
    }
  })

  logger.info('Daily digest job scheduled (runs daily at 9 AM)')
}

