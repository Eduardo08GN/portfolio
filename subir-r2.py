# -*- coding: utf-8 -*-
r"""Sobe os videos do portfolio para o bucket R2 e aponta a pagina para la'.

    set R2_ACCESS_KEY_ID=...
    set R2_SECRET_ACCESS_KEY=...
    python subir-r2.py --base https://<o dominio publico do bucket>

O que ele faz, nesta ordem:
  1. manda cada mp4 de `v/` para o bucket, com Content-Type e Cache-Control certos;
  2. confere o tamanho do que chegou contra o arquivo local (HEAD depois do PUT);
  3. reescreve os `src=` da pagina para a base publica informada;
  4. so' entao apaga `v/` do repositorio — nunca antes do passo 2 fechar.

⛔ CREDENCIAL NAO ENTRA NESTE ARQUIVO nem no repositorio: vem por variavel de
ambiente. O token do R2 da acesso de escrita ao bucket inteiro.

⚠️ O `--base` NAO e' o endpoint da API S3
(`...r2.cloudflarestorage.com/portfolioow`): aquele endereco e' autenticado e
devolve 401 para quem abrir a pagina. A base publica e' o dominio personalizado
do bucket, ou o "URL de desenvolvimento publico" (r2.dev), e um dos dois precisa
estar HABILITADO no painel antes de rodar isto.
"""
import argparse, io, mimetypes, os, re, sys

BUCKET = "portfolioow"
CONTA = "b375ec5e5a83512cd4975b1aaabaec03"
ENDPOINT = "https://%s.r2.cloudflarestorage.com" % CONTA
# os mp4 nunca mudam de conteudo sem mudar de nome: pode cachear por um ano
CACHE = "public, max-age=31536000, immutable"


def cliente():
    import boto3
    from botocore.config import Config
    ak = os.environ.get("R2_ACCESS_KEY_ID")
    sk = os.environ.get("R2_SECRET_ACCESS_KEY")
    if not ak or not sk:
        sys.exit("falta R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY no ambiente")
    return boto3.client("s3", endpoint_url=ENDPOINT, aws_access_key_id=ak,
                        aws_secret_access_key=sk, region_name="auto",
                        config=Config(signature_version="s3v4",
                                      retries={"max_attempts": 5, "mode": "standard"}))


def subir(s3, pasta, prefixo):
    enviados = []
    for nome in sorted(os.listdir(pasta)):
        local = os.path.join(pasta, nome)
        if not os.path.isfile(local):
            continue
        chave = prefixo + nome
        tipo = mimetypes.guess_type(nome)[0] or "application/octet-stream"
        tam = os.path.getsize(local)
        with open(local, "rb") as f:
            s3.put_object(Bucket=BUCKET, Key=chave, Body=f,
                          ContentType=tipo, CacheControl=CACHE)
        # ⭐ conferir e' o passo que autoriza apagar o local depois
        h = s3.head_object(Bucket=BUCKET, Key=chave)
        if h["ContentLength"] != tam:
            sys.exit("TAMANHO DIFERENTE em %s: %d local, %d no bucket"
                     % (chave, tam, h["ContentLength"]))
        print("  %-52s %6.1f MB  %s" % (chave, tam / 1048576, tipo))
        enviados.append((chave, tam))
    return enviados


def apontar(pagina, base, prefixo):
    """Troca `src="v/x.mp4"` por `src="<base>/<prefixo>x.mp4"` na pagina."""
    t = io.open(pagina, encoding="utf-8").read()
    base = base.rstrip("/")
    novo, n = re.subn(r'(src|poster)="v/([^"]+)"',
                      lambda m: '%s="%s/%s%s"' % (m.group(1), base, prefixo, m.group(2)), t)
    io.open(pagina, "w", encoding="utf-8", newline="\n").write(novo)
    return n


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True, help="dominio PUBLICO do bucket (nao o endpoint da API)")
    p.add_argument("--prefixo", default="v/", help="pasta dentro do bucket (padrao: v/)")
    p.add_argument("--apagar-local", action="store_true",
                   help="remove v/ do repositorio depois de conferir o que subiu")
    a = p.parse_args()

    if "r2.cloudflarestorage.com" in a.base:
        sys.exit("--base esta' apontando para o endpoint autenticado da API S3.\n"
                 "Use o dominio publico do bucket (personalizado ou r2.dev).")

    s3 = cliente()
    print("subindo v/ -> %s/%s" % (BUCKET, a.prefixo))
    enviados = subir(s3, "v", a.prefixo)
    print("%d arquivos, %.1f MB" % (len(enviados), sum(t for _, t in enviados) / 1048576))

    n = apontar("index.html", a.base, a.prefixo)
    print("index.html: %d enderecos apontados para %s" % (n, a.base))

    if a.apagar_local:
        for nome in os.listdir("v"):
            os.remove(os.path.join("v", nome))
        os.rmdir("v")
        print("v/ removido do repositorio")


if __name__ == "__main__":
    main()
