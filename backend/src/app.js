import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import rateLimit from 'express-rate-limit'
import { connectDB } from './db/connection.js'
import { errorHandler } from './utils/errorHandler.js'
import { logger } from './utils/logger.js'

// Import routes
import authRoutes from './api/routes/auth.routes.js'
import userRoutes from './api/routes/user.routes.js'
import paperRoutes from './api/routes/paper.routes.js'
import alertRoutes from './api/routes/alert.routes.js'
import articlesRoutes from './api/routes/articles.js'

const app = express()

// Security middleware
app.use(helmet())
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3001',
  credentials: true
}))

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
})
app.use('/api/', limiter)

// Body parsing middleware
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true, limit: '10mb' }))

// Database connection
if (process.env.MONGO_URI || process.env.MONGODB_URI) {
  connectDB()
}

// Health check
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', message: 'Health AI Platform API is running' })
})

// API routes
app.use('/api/auth', authRoutes)
app.use('/api/users', userRoutes)
app.use('/api/papers', paperRoutes)
app.use('/api/alerts', alertRoutes)
app.use('/api/articles', articlesRoutes)

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' })
})

// Error handling middleware (must be last)
app.use(errorHandler)

export default app

