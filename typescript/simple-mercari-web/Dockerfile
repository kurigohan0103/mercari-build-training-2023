FROM node:16-alpine
WORKDIR /home/node/app

RUN addgroup -S mercari && adduser -S trainee -G mercari

COPY src src
COPY node_modules node_modules
COPY public public
COPY package-lock.json package-lock.json
COPY package.json package.json
COPY tsconfig.json tsconfig.json

RUN npm ci

CMD ["npm", "start"]