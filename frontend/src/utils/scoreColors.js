/**
 * Get color classes based on score value
 * @param {number} score - Score value (0-100)
 * @returns {string} Tailwind CSS color classes
 */
export function getScoreColor(score) {
  if (score >= 80) {
    return 'text-green-600 bg-green-100'
  } else if (score >= 60) {
    return 'text-yellow-600 bg-yellow-100'
  } else if (score >= 40) {
    return 'text-orange-600 bg-orange-100'
  } else {
    return 'text-red-600 bg-red-100'
  }
}

/**
 * Get score label based on value
 * @param {number} score - Score value (0-100)
 * @returns {string} Score label
 */
export function getScoreLabel(score) {
  if (score >= 80) return 'Excellent'
  if (score >= 60) return 'Good'
  if (score >= 40) return 'Fair'
  return 'Poor'
}

