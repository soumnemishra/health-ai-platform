/**
 * Calculate relevance score for papers
 * @param {Object} paper - Paper object
 * @param {Object} userPreferences - User preferences
 * @returns {number} Score between 0-100
 */
export function calculateRelevanceScore(paper, userPreferences) {
  let score = 0

  // Base score from paper metadata
  if (paper.citations) {
    score += Math.min(paper.citations / 100, 30) // Max 30 points for citations
  }

  if (paper.publicationDate) {
    const daysSincePublication = (Date.now() - new Date(paper.publicationDate)) / (1000 * 60 * 60 * 24)
    const recencyScore = Math.max(0, 30 - (daysSincePublication / 365) * 10)
    score += recencyScore // Max 30 points for recency
  }

  // User preference matching
  if (userPreferences?.keywords && paper.keywords) {
    const matchingKeywords = paper.keywords.filter(k => 
      userPreferences.keywords.some(uk => 
        k.toLowerCase().includes(uk.toLowerCase())
      )
    )
    score += (matchingKeywords.length / userPreferences.keywords.length) * 40 // Max 40 points
  }

  return Math.min(100, Math.round(score))
}

/**
 * Get score color category
 * @param {number} score - Score value (0-100)
 * @returns {string} Color category
 */
export function getScoreCategory(score) {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'fair'
  return 'poor'
}

