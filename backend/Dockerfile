FROM node:22.22.0-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY tsconfig.json ./
COPY src ./src
RUN npm run build && npm prune --omit=dev
FROM node:22.22.0-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/dist ./dist
COPY --chown=node:node migrations ./migrations
COPY --chown=node:node seeds ./seeds
COPY --chown=node:node package.json ./
USER node
EXPOSE 8181 8182 8183 8184
CMD ["node", "dist/main.js"]
