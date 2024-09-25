 # Base Image
 FROM node:18-alpine

 # Set working directory
 WORKDIR /app

 # Install app dependencies
 COPY package*.json ./
 RUN npm install

 # Copy app files
 COPY . .

 # Build app
 RUN npm run build

 # Expose port
 EXPOSE 3001

 # Start app
 CMD ["npm", "run", "start"]