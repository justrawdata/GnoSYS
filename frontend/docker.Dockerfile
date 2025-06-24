FROM node:20-alpine
WORKDIR /app
COPY . /app
RUN npm install next react react-dom
EXPOSE 3000
CMD ["npx", "next", "dev", "-H", "0.0.0.0"]
