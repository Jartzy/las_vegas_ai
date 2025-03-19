# Las Vegas AI Event Platform

A modern web application for discovering and booking events in Las Vegas, powered by AI recommendations.

## Features

- 🎭 Browse events by category (shows, concerts, sports, etc.)
- 📍 Interactive maps with venue locations
- 💰 Price range filtering
- 📅 Date-based event search
- ⭐ User reviews and ratings
- 🎫 Direct ticket booking
- 📱 Responsive design for all devices

## Tech Stack

- Frontend:
  - React with TypeScript
  - Vite for build tooling
  - Material-UI for components
  - Tailwind CSS for styling
  - React Router for navigation
  - Google Maps integration
- Backend:
  - Python with FastAPI
  - PostgreSQL database
  - Docker containerization
  - AI-powered recommendations

## Prerequisites

- Node.js (v16 or higher)
- Docker and Docker Compose
- Google Maps API key

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/las_vegas_ai.git
cd las_vegas_ai
```

2. Set up environment variables:

Create a `.env` file in the frontend directory:
```bash
# frontend/.env
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

Create a `.env` file in the root directory:
```bash
# .env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
```

3. Install dependencies:
```bash
# Frontend dependencies
cd frontend
npm install

# Return to root directory
cd ..
```

## Development

Start the development environment:
```bash
docker compose up
```

This will start:
- Frontend at http://localhost:5173
- Backend API at http://localhost:5001
- PostgreSQL database at localhost:5432

## API Documentation

The API documentation is available at http://localhost:5001/docs when running the development server.

## Component Documentation

### Map Component

The Map component provides an interactive Google Maps interface for displaying event locations.

```typescript
import { Map } from './components/Map';

// Usage
<Map
  latitude={36.1699}
  longitude={-115.1398}
  zoom={14}
  markers={[
    {
      latitude: 36.1699,
      longitude: -115.1398,
      title: "Event Location"
    }
  ]}
/>
```

Props:
- `latitude`: number (required) - Center latitude
- `longitude`: number (required) - Center longitude
- `zoom`: number (optional) - Zoom level (default: 14)
- `markers`: Array (optional) - List of markers to display

## Environment Variables

### Frontend (.env)
- `VITE_GOOGLE_MAPS_API_KEY`: Google Maps API key for map integration

### Backend (.env)
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## Commit Message Convention

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 