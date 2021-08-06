# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node as builder

WORKDIR /app

# to reduce npm install time
COPY ./app/package*.json .

RUN npm install

COPY ./app /app

RUN npm run build:prod


# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:alpine

COPY --from=builder /app/dist/ /usr/share/nginx/html
COPY /nginx.conf /etc/nginx/conf.d/default.conf