# Stage 1: Build
FROM node:20-alpine AS build

WORKDIR /app

RUN apk add --no-cache make

COPY package-lock.json package.json Makefile ./

RUN make install

COPY . .

RUN make build

# Stage 2: Serve
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

LABEL org.opencontainers.image.source="https://github.com/w0rmr1d3r/finance-tracker/tree/main/frontend" \
      org.opencontainers.image.licenses="MIT"

CMD ["nginx", "-g", "daemon off;"]
