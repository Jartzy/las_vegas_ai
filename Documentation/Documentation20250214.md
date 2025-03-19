# Las VAIgas: AI-Powered Vegas Experience Recommender

## 🌟 Project Overview

Las VAIgas is an innovative AI-driven platform designed to revolutionize how users explore and experience Las Vegas. Combining machine learning, real-time event tracking, and personalized recommendations, the application provides an intelligent guide to the best attractions, events, and experiences in Las Vegas.

## ✨ Key Features

- 🔐 Secure Authentication with Two-Factor Authentication (2FA)
- 🤖 AI-Powered Personalized Recommendations
- 📅 Real-time Event Tracking
- 🎲 Comprehensive Las Vegas Event Database
- 📊 User Interaction & Feedback System

## 🚀 Tech Stack

### Backend
- Flask
- PostgreSQL
- SQLAlchemy
- Machine Learning Models

### Frontend
- React
- TypeScript
- Tailwind CSS
- Vite

### DevOps
- Docker
- Nginx
- CI/CD via GitHub Actions

## 📦 Project Structure

```
las_vegas_ai/
├── backend/                 # Flask Backend
│   ├── app.py               # Main application
│   ├── auth.py              # Authentication logic
│   ├── recommendations.py   # AI recommendation engine
│   └── ...
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── ...
└── docker-compose.yml       # Container orchestration
```

## 🛠 Local Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker (optional)

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
flask run
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/login`: User login
- `POST /api/auth/verify-otp`: Two-factor authentication
- `POST /api/auth/register`: User registration

### Recommendations
- `GET /api/recommendations`: Fetch personalized recommendations
- `POST /api/recommendations/feedback`: Submit recommendation feedback

## 🐳 Docker Deployment
```bash
docker-compose build
docker-compose up
```

## 🧪 Testing
- Backend: pytest
- Frontend: Jest & React Testing Library

## 🔜 Roadmap
- [ ] Mobile App Development
- [ ] Enhanced AI Recommendation Models
- [ ] Social Media Integration
- [ ] Multilingual Support

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push and create a Pull Request

## 📄 License
MIT License

## 🚨 Support
For issues or questions, please open a GitHub issue.
```

This README provides a comprehensive overview of the Las VAIgas project, including its features, tech stack, setup instructions, and contribution guidelines. It's designed to be both informative for potential users and helpful for developers who want to understand or contribute to the project.

Would you like me to make any specific modifications to the documentation?