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

# Set environment variables to disable WebSocket
ENV WDS_SOCKET_HOST=0.0.0.0
ENV WDS_SOCKET_PORT=0  
ENV FAST_REFRESH=false
ENV GENERATE_SOURCEMAP=false

# Run in development mode (like your successful deployment)
CMD ["npm", "start"]
