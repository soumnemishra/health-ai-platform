import dotenv from 'dotenv'

dotenv.config()

export const config = {
  // Server config
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  
  // Database
  mongodbUri: process.env.MONGODB_URI || 'mongodb://localhost:27017/health_ai',
  
  // JWT
  jwtSecret: process.env.JWT_SECRET || 'your-secret-key-change-in-production',
  jwtExpire: process.env.JWT_EXPIRE || '7d',
  
  // CORS
  frontendUrl: process.env.FRONTEND_URL || 'http://localhost:3001',
  
  // ML Service
  mlServiceUrl: process.env.ML_SERVICE_URL || 'http://localhost:5000',
  
  // Rate limiting
  rateLimitWindow: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000,
  rateLimitMax: parseInt(process.env.RATE_LIMIT_MAX) || 100,
}

