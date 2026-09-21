# Leia isto primeiro

Este repositório existe para **ser recortado**. Ele publica o portfólio do Organic
Wave Studio — doze vídeos verticais 9:16 com player inline — e o mesmo bloco é
feito para ser colado dentro de outra página.

**Se você chegou aqui para enxertar o bloco numa landing, o arquivo que você
precisa é [`INCORPORAR.md`](INCORPORAR.md).** Ele diz o que copiar, o que não pode
mudar e por quê. Não deduza pela leitura do `index.html`: três das decisões de lá
parecem arbitrárias e não são.

## O mínimo para se localizar

- `index.html` — a página inteira, sem build. O bloco recortável está entre os
  marcadores `OW:INICIO DO TRECHO` e `OW:FIM DO TRECHO`.
- `teste-em-landing-hostil.html` — o bloco colado numa landing de propósito
  agressiva. É o teste de regressão: se os dois lados sobrevivem, a blindagem está
  de pé.
- Os vídeos, as capas e o logotipo **não estão aqui**: moram num bucket R2 público,
  com URL absoluta dentro do trecho. Nada para baixar.
- `subir-r2.py` — só serve para publicar mídia nova no bucket. Precisa de chaves
  que não estão no repositório.

## Três regras que valem para qualquer mexida

1. **Tudo é prefixado `ow-` e ancorado em `.ow-portfolio`.** É o que impede o bloco
   de repintar a página de quem recebe. Se renomear, renomeie no CSS, no HTML e no
   script — a classe `.ow-play` e o método `video.play()` são o mesmo texto, e um
   replace global quebra o player.
2. **`preload="none"` fica.** É o que faz a página abrir sem baixar um byte de vídeo.
3. **A regra `.ow-portfolio :where(...)` fica onde está**, antes dos componentes. O
   `:where()` zera a especificidade de propósito; movê-la para baixo desmonta o
   desenho. O porquê está no comentário dela e em `INCORPORAR.md`.
