# Como colar este portfólio numa outra página

Este arquivo é para **o agente que vai enxertar o bloco numa landing**. Se você é
esse agente: leia até o fim antes de editar qualquer coisa. São cinco minutos e
evitam os três erros que já aconteceram aqui.

O que você vai colar é a vitrine do Organic Wave Studio: um cabeçalho com a marca
e uma grade de doze vídeos verticais 9:16 com player inline próprio.

---

## 1. O que copiar

Abra [`index.html`](index.html) e procure estes dois marcadores:

```
<!-- ═══ OW:INICIO DO TRECHO ═══ -->
...
<!-- ═══ OW:FIM DO TRECHO ═══ -->
```

Entre eles há **quatro pedaços, nesta ordem**. Copie os quatro, sem pular nenhum:

| # | o quê | onde colar |
|---|---|---|
| 1 | `<style>` | junto do bloco, ou no `<head>` — tanto faz |
| 2 | `<div class="ow-portfolio">` | onde a seção deve aparecer na landing |
| 3 | `<template id="ow-molde-barra">` | em qualquer lugar do `<body>` |
| 4 | `<script>` | depois do `<div>` e do `<template>` |

⛔ **O `<template>` não é opcional.** É dele que sai a barra de controle de cada
vídeo; sem ele a grade aparece, mas nenhum player tem botão nem barra de posição.
Foi o pedaço esquecido na primeira tentativa.

**Não copie** o `<style>` que está no `<head>` do `index.html` — aquele é só o chão
escuro da página de demonstração e está marcado como tal. Na landing, o chão é dela.

---

## 2. As mídias já estão hospedadas — não as republique

Os doze vídeos, as doze capas e o logotipo estão num bucket Cloudflare R2 público:

```
https://pub-a64ff07a02a446df8b492d42e886c18b.r2.dev/
  v/*.mp4          os doze vídeos (720×1280 e 540×960, H.264 + AAC)
  p/*.jpg          as doze capas
  assets/logo-ow.webp   a marca
```

As URLs já estão absolutas dentro do trecho: **funciona em qualquer domínio, sem
copiar arquivo nenhum**. Não baixe e re-hospede — some com o cache e dobra o custo
à toa. O bucket serve com `Cache-Control` de um ano e responde a faixas de bytes
(`206`), que é o que faz arrastar a barra do player pular direto para o trecho em
vez de baixar o mp4 inteiro.

---

## 3. O que você NÃO deve mudar

Cada item aqui é uma cicatriz, não uma preferência.

**`preload="none"` nos doze `<video>`.** É o que faz a página abrir com doze JPEG e
**zero byte de vídeo**. Trocar por `metadata` ou `auto` custa dezenas de MB no
primeiro carregamento da landing. O vídeo só começa a baixar quando alguém clica.

**O "toca um por vez".** A função `assumir()` no script pausa qualquer outro vídeo
antes de começar um novo. Doze vídeos com som na mesma tela é barulho, não vitrine.

**O `IntersectionObserver` do fim do script.** Pausa o vídeo que sai da tela. Sem
ele, o visitante rola a página e continua ouvindo alguém falando de onde não vê.

**Os prefixos `ow-`.** Toda classe, toda variável CSS (`--ow-*`) e o `@keyframes
ow-girar` estão prefixados, e todo seletor está ancorado em `.ow-portfolio`. Não é
firula: é o que impede o bloco de repintar a landing inteira. Se você renomear,
renomeie nos três lugares (CSS, HTML e o script).

**A regra `.ow-portfolio :where(...)`, e a posição dela.** O `:where()` zera a
especificidade de propósito: essa regra ganha de um `h1{color:...}` da landing
(0,0,1) e perde de qualquer classe `.ow-` (0,1,0). Se você movê-la para depois dos
componentes, ela passa a ganhar deles e o desenho desmonta. Ela existe porque
propriedade **herdada** perde para qualquer regra do hospedeiro — sem ela, numa
landing com `h1{color:#c2410c}` o título "Doze peças" sai laranja. Aconteceu.

---

## 4. O que você pode mudar à vontade

**As tags.** O estilo do título vem da classe `.ow-titulo`, não da tag. Se a landing
já tem um `<h1>`, troque o nosso por `<h2>` ou `<p>` — a aparência não muda. Vale o
mesmo para `.ow-titulo-secao`.

**As cores e as fontes.** Estão todas em variáveis, no primeiro bloco do CSS:

```css
.ow-portfolio{
  --ow-breu:#060E0D;   /* chão do bloco     */
  --ow-creme:#F0EDE2;  /* texto             */
  --ow-onda:#5FD6CE;   /* acento            */
  --ow-areia:#D2A96A;  /* acento secundário */
  ...
}
```

⚠️ Mas leia isto antes de clarear o fundo: **o logotipo tem o W em creme
(`#F0EDE2`) e some em fundo claro.** O bloco é escuro de propósito. Se a landing é
clara, mantenha o bloco escuro como uma faixa — é o que a página de teste faz, e
fica bom. Se precisar mesmo de fundo claro, tire o logotipo do cabeçalho e use só
a assinatura do rodapé; **não** ponha uma chapa escura atrás da marca, isso já foi
tentado e suja o cabeçalho.

**O texto.** Cabeçalho, números do trilho e legendas dos cartões são conteúdo comum,
em português. As frases dentro das aspas em cada cartão são a **primeira fala real
de cada vídeo**, transcrita do áudio — se traduzir, não invente: elas conferem com
o que se ouve.

**Quantos vídeos aparecem.** Cada cartão é um `<article class="ow-peca">` fechado
em si. Apague os que não quiser; a grade se reorganiza sozinha. Se cortar, ajuste
os números do trilho (`Peças`, `Duração total`) — eles estão escritos na mão.

**O número de colunas.** `.ow-grade` faz 3 / 2 / 1 em 960px e 600px. Se a landing
tem menos largura útil, mude o `grid-template-columns`.

---

## 5. Se a landing não for HTML puro

O bloco é HTML + CSS + JS sem dependência nenhuma. Para levar para outro stack:

- **React / Next / Vue / Svelte** — o markup vira componente quase direto. O único
  cuidado é o script: ele roda uma vez sobre `.ow-portfolio .ow-peca` e monta as
  barras a partir do `<template>`. Em React, chame esse mesmo código dentro de um
  `useEffect(() => {...}, [])`, ou reescreva os handlers como props. Em Next com
  SSR, ele precisa rodar só no cliente.
- **Tailwind** — não converta as classes. Mantenha o `<style>` como está; ele não
  conflita com utilitários porque tudo está escopado.
- **Construtor visual (Webflow, Framer, WordPress)** — cole os quatro pedaços num
  bloco de "HTML embed" único, na ordem.

Em qualquer caso, **teste o clique num vídeo** antes de dar por pronto. Se a grade
aparece mas nada toca, faltou o `<template>` ou o script não rodou.

---

## 6. A prova de que não vaza

Abra [`teste-em-landing-hostil.html`](teste-em-landing-hostil.html). É uma landing
deliberadamente agressiva — tema claro, Georgia, e regras globais com os mesmos
nomes genéricos que o template usava antes (`h1`, `button`, `img,video`, `.grade`,
`.peca`, `.nota`, `.barra`, `@keyframes girar`, `*{box-sizing:content-box}`) — com
o trecho colado no meio.

Se depois das suas mudanças a landing continuar com o título laranja em Georgia, o
botão verde e a borda tracejada, **e** o bloco continuar escuro com o título creme
e os vídeos sem borda laranja, você não quebrou a blindagem. Se algum dos dois
lados mudar, quebrou.

---

## 7. Teclado e acessibilidade

Já está feito, não precisa acrescentar:

- com o cartão em foco: `espaço` ou `K` toca/pausa, `M` tira o som, `F` tela cheia;
- com a barra de posição em foco: `←` `→` andam 5 s, `PageUp`/`PageDown` 10 s,
  `Home`/`End` vão para as pontas;
- a barra é um `role="slider"` de verdade, com `aria-valuenow` e `aria-valuetext`
  atualizados a cada quadro;
- todo botão tem `aria-label` que muda com o estado (Tocar/Pausar, Tirar/Ligar o som);
- `prefers-reduced-motion` desliga as transições;
- alvo de toque de 44 px abaixo de 600 px de largura;
- contraste conferido: 15,0:1 no texto, 5,9:1 na linha de meta.

---

## 8. Se precisar trocar os vídeos

Isso é trabalho do lado do Organic Wave, não da landing. Os arquivos sobem com
`subir-r2.py` (está no repositório, precisa das chaves do bucket) e o endereço
público não muda. Fale com o Eduardo.
