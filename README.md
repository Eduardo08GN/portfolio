# Organic Wave Studio — portfólio

Página única com as doze peças escolhidas do estúdio. Vídeo vertical 9:16, player
inline próprio, tema escuro. É o template `preview-inline-player` da ferramenta,
levado ao nível de vitrine pública.

**No ar:** ver o domínio da aplicação `ow-portfolio` no Coolify.

## O que tem aqui

```
index.html      a página inteira — HTML, CSS e JS num arquivo só, sem build
assets/         o mark da marca (webp servido; png é o master do upscale 4×)
p/              as capas (poster de cada vídeo, 540 px de largura, JPEG)
v/              os doze mp4 na versão de web
Dockerfile      nginx alpine servindo estático
nginx.conf      faixas de bytes, cache e gzip
_manifesto.json o que foi medido de cada vídeo (duração, dimensão, tamanho)
```

## Decisões que não são óbvias

**Tema único escuro, de propósito.** O mark da Organic Wave tem o W em creme
(`#F0EDE2`). Sobre qualquer fundo claro ele some. A saída tentada antes — pôr um
disco escuro atrás do logotipo — só sujou o cabeçalho. Então a página inteira
commita no escuro e pinta todas as cores explicitamente, em vez de fingir que
suporta os dois temas.

**A paleta sai do próprio ativo.** `#F0EDE2` é o creme do W, `#5FD6CE` é a
turquesa da onda e `#D2A96A` é o anel dourado — todos amostrados do arquivo, não
escolhidos por fora.

**O logotipo original tem 160×138.** Para caber grande no cabeçalho ele foi
ampliado 4× com Lanczos, com o canal alfa reapertado depois (o Lanczos deixa
meio-tom nas quinas do W e a letra fica mole). O resultado está em
`assets/logo-ow.png`; o `.webp` é o que a página serve.

**Os mp4 daqui não são os arquivos de entrega.** São recodificações para web
(CRF 26, `+faststart`): 83 MB viraram 44 MB sem diferença visível numa grade.
Os originais continuam no disco de produção.

**`preload="none"` em todos os doze.** A página abre com doze JPEG e nenhum byte
de vídeo; o mp4 só começa a carregar quando alguém clica. Sem isso, abrir a
página custaria dezenas de MB.

**Toca um por vez.** Doze vídeos com som na mesma tela é barulho. Quem começa
cala os outros, e quem sai da tela pausa sozinho (`IntersectionObserver`).

## Teclado

Com o cartão em foco: `espaço` ou `K` toca/pausa, `M` tira o som, `F` tela cheia.
Com a barra de posição em foco: `←` `→` andam 5 s, `PageUp`/`PageDown` 10 s,
`Home`/`End` vão para as pontas.

## Rodar local

```bash
python -m http.server 8765
```

Ou como vai para o ar:

```bash
docker build -t ow-portfolio . && docker run --rm -p 8080:80 ow-portfolio
```
