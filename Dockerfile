# Portfolio do Organic Wave Studio: pagina estatica + 12 mp4 servidos por nginx.
# Nao ha build: o que esta no repositorio e' exatamente o que vai para o ar.
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY assets/    /usr/share/nginx/html/assets/
COPY p/         /usr/share/nginx/html/p/
COPY v/         /usr/share/nginx/html/v/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=4s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/healthz || exit 1
