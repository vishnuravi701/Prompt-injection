FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Install serve to run the build
RUN npm install -g serve

# Start application
CMD ["serve", "-s", "dist", "-l", "3000"]
