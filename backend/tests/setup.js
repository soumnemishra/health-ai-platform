// Test setup file
// Configure test environment

process.env.NODE_ENV = 'test'
process.env.MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/health_ai_test'
process.env.JWT_SECRET = 'test-secret-key'

