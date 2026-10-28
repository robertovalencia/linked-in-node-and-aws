FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
FROM nginxinc/nginx-unprivileged:1.31-alpine
ENV DNS_RESOLVER=127.0.0.11 \
    IDENTITY_UPSTREAM=identity \
    CATALOG_UPSTREAM=catalog \
    INQUIRIES_UPSTREAM=inquiries \
    NOTIFICATIONS_UPSTREAM=notifications \
    NGINX_ENVSUBST_FILTER="^(DNS_RESOLVER|IDENTITY_UPSTREAM|CATALOG_UPSTREAM|INQUIRIES_UPSTREAM|NOTIFICATIONS_UPSTREAM)$"
COPY --chmod=755 10-validate-dns.sh /docker-entrypoint.d/10-validate-dns.sh
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8180
HEALTHCHECK --interval=10s --timeout=3s CMD wget -q -O /dev/null http://127.0.0.1:8180/health || exit 1
