/**
 * Format a date to a readable string
 * @param {Date|string} date - Date object or date string
 * @param {string} format - Format type ('short', 'long', 'relative')
 * @returns {string} Formatted date string
 */
export function formatDate(date, format = 'short') {
  const dateObj = date instanceof Date ? date : new Date(date)
  
  if (isNaN(dateObj.getTime())) {
    return 'Invalid Date'
  }

  switch (format) {
    case 'short':
      return dateObj.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    
    case 'long':
      return dateObj.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    
    case 'relative':
      const now = new Date()
      const diffInSeconds = Math.floor((now - dateObj) / 1000)
      
      if (diffInSeconds < 60) return 'just now'
      if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`
      if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`
      if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`
      
      return dateObj.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    
    default:
      return dateObj.toLocaleDateString()
  }
}

