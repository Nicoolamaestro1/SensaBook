FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install Expo CLI globally
RUN npm install -g @expo/cli

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port for web development
EXPOSE 8081

# Command to start the development server
CMD ["npx", "expo", "start", "--web", "--port", "8081"] 