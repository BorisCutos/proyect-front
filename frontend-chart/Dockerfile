# Dockerfile para Frontend
FROM nginx:alpine

# Crear directorios necesarios y darles permisos apropiados
RUN mkdir -p /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    /var/run \
    && chmod -R 777 /var/cache/nginx \
    && chmod -R 777 /var/run \
    && chmod -R 777 /etc/nginx \
    && touch /var/run/nginx.pid \
    && chmod 777 /var/run/nginx.pid

# Crear configuración de nginx para puerto 8080 (OpenShift no permite puertos < 1024)
RUN echo 'server {' > /etc/nginx/conf.d/default.conf && \
    echo '    listen 8080;' >> /etc/nginx/conf.d/default.conf && \
    echo '    server_name localhost;' >> /etc/nginx/conf.d/default.conf && \
    echo '    location / {' >> /etc/nginx/conf.d/default.conf && \
    echo '        root /usr/share/nginx/html;' >> /etc/nginx/conf.d/default.conf && \
    echo '        index index.html;' >> /etc/nginx/conf.d/default.conf && \
    echo '        try_files $uri $uri/ /index.html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    }' >> /etc/nginx/conf.d/default.conf && \
    echo '}' >> /etc/nginx/conf.d/default.conf

# Copiar archivos HTML
COPY index.html /usr/share/nginx/html/

# Dar permisos a todo el directorio HTML
RUN chmod -R 777 /usr/share/nginx/html

# Exponer puerto 8080 (en lugar de 3000)
EXPOSE 8080

# Ejecutar nginx como proceso foreground
CMD ["nginx", "-g", "daemon off;"]
