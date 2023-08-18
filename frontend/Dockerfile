# this is a temporary image for using npm to build the frontend
# it is superseded by the next FROM statement, but we can (and do) copy stuff from it

# From starts a new image
FROM node:alpine AS builder_image

# no mkdir needed
WORKDIR /builder

# needed for the npm install below
COPY package*.json ./

# install pre-req packages
RUN npm install
RUN npm install -g npm@9.8.1

# COPY the frontend source code here
COPY public/ ./public
COPY src/ ./src

# build the application
RUN npm run build

# Expose port 3000 for the frontend
EXPOSE 3000

# Start the npm to let port 3000 run
CMD [ "npm", "start"]
