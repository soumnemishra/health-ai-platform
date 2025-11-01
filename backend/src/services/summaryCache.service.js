import { logger } from '../utils/logger.js'
import axios from 'axios'

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:5000'
const cache = new Map() // In-memory cache (consider using Redis for production)

/**
 * Get or generate summary for a paper
 * @param {string} paperId - Paper ID
 * @param {string} paperContent - Paper content
 * @returns {Promise<string>} Summary text
 */
export async function getSummary(paperId, paperContent) {
  // Check cache first
  if (cache.has(paperId)) {
    logger.info(`Cache hit for paper ${paperId}`)
    return cache.get(paperId)
  }

  try {
    // Call ML service to generate summary
    const response = await axios.post(`${ML_SERVICE_URL}/api/summarize`, {
      paperId,
      content: paperContent
    })

    const summary = response.data.summary
    
    // Cache the summary
    cache.set(paperId, summary)
    
    // Set expiry (24 hours)
    setTimeout(() => {
      cache.delete(paperId)
    }, 24 * 60 * 60 * 1000)

    return summary
  } catch (error) {
    logger.error(`Summary generation error: ${error.message}`)
    throw new Error('Failed to generate summary')
  }
}

/**
 * Invalidate cache for a paper
 * @param {string} paperId - Paper ID
 */
export function invalidateCache(paperId) {
  cache.delete(paperId)
  logger.info(`Cache invalidated for paper ${paperId}`)
}

