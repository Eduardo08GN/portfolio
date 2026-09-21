# Portfolio do Organic Wave Studio: a pagina, o logotipo e as 12 capas.
# Os 12 mp4 NAO entram aqui (ver abaixo) — a imagem fica em ~1 MB.
# Nao ha build: o que esta no repositorio e' exatamente o que vai para o ar.
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
# a prova de que o bloco nao vaza, aberta no navegador de quem for enxertar
COPY teste-em-landing-hostil.html /usr/share/nginx/html/teste-em-landing-hostil.html
COPY assets/    /usr/share/nginx/html/assets/
COPY p/         /usr/share/nginx/html/p/
# os mp4 NAO entram na imagem: moram no bucket R2 `portfolioow` e sao servidos
# direto de la'. Ver README > Onde ficam os videos.

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=4s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/healthz || exit 1
