# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node

WORKDIR /app

# to reduce npm install time
COPY ./app/package*.json .

RUN npm install

CMD npm run dev