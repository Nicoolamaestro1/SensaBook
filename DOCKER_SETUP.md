# 🐳 SensaBook Docker Setup

This guide will help you set up and run SensaBook using Docker on your local machine.

## 📋 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) (usually comes with Docker Desktop)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SensaBook
```

### 2. Start All Services
```bash
docker-compose up --build
```

This will start:
- **PostgreSQL Database** on port 5432
- **Backend API** on port 8000
- **Frontend (Mobile App)** on port 8081

### 3. Access the Application

- **Frontend (Mobile App):** http://localhost:8081
- **Backend API Docs:** http://localhost:8000/docs
- **Database:** PostgreSQL on localhost:5432

## 🔧 Development Workflow

### Start Services in Background
```bash
docker-compose up -d
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Stop Services
```bash
docker-compose down
```

### Rebuild After Code Changes
```bash
docker-compose up --build
```

## 🛠️ Individual Service Management

### Backend Only
```bash
# Start backend with database
docker-compose up postgres backend

# Rebuild backend only
docker-compose build backend
docker-compose up backend
```

### Frontend Only
```bash
# Start frontend (requires backend to be running)
docker-compose up frontend
```

## 🗄️ Database Management

### Access PostgreSQL
```bash
# Connect to database
docker-compose exec postgres psql -U user -d sensabook

# View database logs
docker-compose logs postgres
```

### Reset Database
```bash
# Remove database volume
docker-compose down -v
docker-compose up --build
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   netstat -an | findstr :8000
   # or
   lsof -i :8000
   
   # Stop the conflicting service
   ```

2. **Database Connection Issues**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   
   # Restart database
   docker-compose restart postgres
   ```

3. **Build Failures**
   ```bash
   # Clean build
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

### View Service Status
```bash
docker-compose ps
```

### Access Container Shell
```bash
# Backend container
docker-compose exec backend bash

# Frontend container
docker-compose exec frontend sh
```

## 📝 Environment Variables

The following environment variables are configured in `docker-compose.yml`:

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Frontend
- `REACT_APP_API_URL`: Backend API URL

## 🔐 Security Notes

- The default `SECRET_KEY` in docker-compose.yml should be changed for production
- Database credentials are set to default values for development
- Consider using environment files for sensitive data in production

## 📱 Testing the Application

1. **Open the frontend:** http://localhost:8081
2. **Register a new user** or use existing credentials
3. **Test the login functionality**
4. **Check API documentation:** http://localhost:8000/docs

## 🧹 Cleanup

### Remove All Containers and Volumes
```bash
docker-compose down -v
docker system prune -f
```

### Remove Only Containers (Keep Volumes)
```bash
docker-compose down
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Expo Documentation](https://docs.expo.dev/)

---

**Happy Coding! 🎉** 