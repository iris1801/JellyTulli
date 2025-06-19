# Fase 1: Build dell'applicazione React
FROM node:18-alpine AS build

WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# Fase 2: Immagine per servire il frontend con Nginx
FROM nginx:alpine
# Copia i file statici generati nel build di React
COPY --from=build /app/build /usr/share/nginx/html
# Copia la configurazione Nginx per il proxy delle API
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Espone la porta 80 per il frontend
EXPOSE 80

# Avvia Nginx
CMD ["nginx", "-g", "daemon off;"]
