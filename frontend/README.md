# Health AI Platform - Frontend

React-based frontend application for the Health AI Platform, built with Vite and Tailwind CSS.

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **React Context API** - State management

## Project Structure

```
frontend/
├── src/
│   ├── api/                  # Axios API clients (calls backend endpoints)
│   ├── assets/               # Images, icons, logos
│   ├── components/           # Reusable UI components (Cards, NavBar, Loader)
│   ├── features/             # Page-level modules (Feed, PaperDetail, Alerts)
│   ├── hooks/                # Custom hooks (useFetch, useAuth)
│   ├── context/              # React Context (UserContext, ThemeContext)
│   ├── pages/                # Routes (Home, Login, Dashboard)
│   ├── routes/               # Route definitions
│   ├── utils/                # Helpers (formatDate, scoreColors)
│   ├── styles/               # Global CSS/Tailwind setup
│   ├── main.jsx              # Entry point
│   └── App.jsx               # Router + layout
├── public/                   # Static assets
├── vite.config.js            # Build config
└── package.json
```

## Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Create `.env.local` file**
   ```env
   VITE_API_URL=http://localhost:3000
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

5. **Preview production build**
   ```bash
   npm run preview
   ```

## Available Scripts

- `npm run dev` - Start development server (http://localhost:3001)
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features

- ✅ Authentication with JWT tokens
- ✅ React Router for navigation
- ✅ Context API for global state
- ✅ Custom hooks for reusable logic
- ✅ Tailwind CSS for styling
- ✅ Dark mode support
- ✅ Responsive design

## API Integration

The frontend uses Axios for API calls. Configure the base URL in `.env.local` or update `src/api/client.js`.

API client automatically:
- Adds authentication tokens to requests
- Handles 401 errors (unauthorized)
- Provides request/response interceptors

