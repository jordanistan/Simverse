# Use the official Node.js LTS (Long-Term Support) version as a base image
FROM node:lts

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and yarn.lock to leverage Docker's layer caching
COPY package.json yarn.lock ./

# Install dependencies using yarn
RUN yarn install

# Copy the rest of the application's source code
COPY . .

# Vite uses port 5173 by default, so we expose it
EXPOSE 5173

# The command to start the Vite development server
# We use --host to ensure it's accessible from outside the container
CMD ["yarn", "dev", "--host"]
