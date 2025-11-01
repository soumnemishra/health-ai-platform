import axios from 'axios'
import { logger } from '../utils/logger.js'

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:5000'

/**
 * Retrieve relevant papers using ML service
 * @param {Object} query - Search query object
 * @returns {Promise<Array>} Array of relevant papers
 */
export async function retrievePapers(query) {
  try {
    const response = await axios.post(`${ML_SERVICE_URL}/api/retrieve`, {
      query: query.text,
      filters: query.filters || {},
      limit: query.limit || 10
    })

    return response.data.papers || []
  } catch (error) {
    logger.error(`Retrieval service error: ${error.message}`)
    throw new Error('Failed to retrieve papers')
  }
}

/**
 * Get paper embeddings for similarity search
 * @param {string} paperId - Paper ID
 * @returns {Promise<Array>} Embedding vector
 */
export async function getPaperEmbedding(paperId) {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/api/embeddings/${paperId}`)
    return response.data.embedding
  } catch (error) {
    logger.error(`Get embedding error: ${error.message}`)
    throw new Error('Failed to get paper embedding')
  }
}

