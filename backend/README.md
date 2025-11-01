# Health AI Platform - Backend

Node.js/Express backend API server for the Health AI Platform.

## Tech Stack

- **Express.js** - Web framework
- **MongoDB/Mongoose** - Database and ODM
- **JWT** - Authentication
- **Joi** - Request validation
- **Winston** - Logging
- **Node-cron** - Scheduled jobs
- **Jest/Supertest** - Testing

## Project Structure

```
backend/
├── src/
│   ├── api/
│   │   ├── routes/           # Express route files (auth, papers, alerts, users)
│   │   ├── controllers/      # Route logic (business rules)
│   │   ├── middleware/       # Auth, rate limiting, validation
│   │   └── validators/       # Joi/Zod schemas for requests
│   ├── models/               # Mongoose models (User, Paper, Feedback, Alert)
│   ├── services/             # Business logic (retrieval service, summary cache)
│   ├── utils/                # Helpers (logger, error handler, scoring utils)
│   ├── config/               # Env and app configs
│   ├── db/                   # MongoDB connection setup
│   ├── jobs/                 # CRON jobs (daily digests, cleanup)
│   ├── app.js                # Express app entry
│   └── server.js             # Launch server, attach middlewares
├── tests/                    # Jest/Supertest integration tests
├── package.json
└── .env
```

## Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Create `.env` file**
   ```env
   PORT=3000
   NODE_ENV=development
   MONGODB_URI=mongodb://localhost:27017/health_ai
   JWT_SECRET=your-secret-key-change-in-production
   JWT_EXPIRE=7d
   FRONTEND_URL=http://localhost:3001
   ML_SERVICE_URL=http://localhost:5000
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Run tests**
   ```bash
   npm test
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

### Users
- `GET /api/users` - Get all users (admin)
- `GET /api/users/:id` - Get user by ID
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user (admin)

### Papers
- `GET /api/papers` - Get all papers
- `GET /api/papers/:id` - Get paper by ID
- `GET /api/papers/search?query=...` - Search papers
- `POST /api/papers` - Create paper (auth required)
- `PUT /api/papers/:id` - Update paper (auth required)
- `DELETE /api/papers/:id` - Delete paper (auth required)

### Alerts
- `GET /api/alerts` - Get user alerts (auth required)
- `GET /api/alerts/:id` - Get alert by ID (auth required)
- `POST /api/alerts` - Create alert (auth required)
- `PUT /api/alerts/:id` - Update alert (auth required)
- `PATCH /api/alerts/:id/read` - Mark alert as read (auth required)
- `DELETE /api/alerts/:id` - Delete alert (auth required)

## Features

- ✅ JWT Authentication
- ✅ Role-based authorization
- ✅ Request validation with Joi
- ✅ Rate limiting
- ✅ Error handling
- ✅ Logging with Winston
- ✅ Scheduled CRON jobs
- ✅ MongoDB integration
- ✅ RESTful API design

## Development

The server runs on `http://localhost:3000` by default. Use `nodemon` for auto-reload during development.

