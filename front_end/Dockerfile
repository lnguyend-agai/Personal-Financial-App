# use Node.js base image
FROM node:16

# Create folder app into container
WORKDIR /app

# Copy file package.json and setting dependencies
COPY package.json .
RUN npm install

# Copy source code into container
COPY . .

# Build React application
RUN npm run build

# Use Nginx for supporting React application
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]