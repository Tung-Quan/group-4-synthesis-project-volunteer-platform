# 1. choose nodejs env
FROM node:22-alpine

# 2. create folder for container
WORKDIR /app

# 3. Copy file for library
COPY package.json package-lock.json ./

# 4. install lib
RUN npm install

# 5. copy all code file of frontend
COPY . .

# 6. open port 5173 for Vite)
EXPOSE 5173

# 7. run frontend ( --host for Docker allowed external access)
CMD ["npm", "run", "dev", "--", "--host"]