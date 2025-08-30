# Frontend Dockerfile - Development mode
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

EXPOSE 3000

# Run in development mode (like your successful deployment)
CMD ["npm", "start"]
