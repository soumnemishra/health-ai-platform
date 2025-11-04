import { createClient } from '@supabase/supabase-js'
import { logger } from '../utils/logger.js'

let supabaseClient = null

// Lazy initialization function
const getSupabaseClient = () => {
  if (supabaseClient) {
    return supabaseClient
  }

  // Get Supabase configuration from environment variables
  const supabaseUrl = process.env.SUPABASE_URL
  const supabaseServiceKey = process.env.SUPABASE_SERVICE_KEY
  const supabaseAnonKey = process.env.SUPABASE_ANON_KEY || process.env.SUPABASE_KEY
  const supabaseKey = supabaseServiceKey || supabaseAnonKey

  // Validate required environment variables
  if (!supabaseUrl) {
    logger.error('SUPABASE_URL environment variable is required')
    throw new Error('SUPABASE_URL environment variable is required')
  }

  if (!supabaseKey) {
    logger.error('SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY (or SUPABASE_KEY) is required')
    throw new Error('SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY (or SUPABASE_KEY) is required')
  }

  // Create Supabase client
  supabaseClient = createClient(supabaseUrl, supabaseKey, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
    },
  })

  logger.info('Supabase client initialized')
  return supabaseClient
}

// Export a getter that lazily initializes the client
export const supabase = new Proxy({}, {
  get(target, prop) {
    const client = getSupabaseClient()
    return client[prop]
  }
})

export default supabase
