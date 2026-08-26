"""Gera img/og-preview.jpg, o card que WhatsApp, Telegram e Facebook mostram
quando o link do site e colado numa conversa.

    pip install Pillow
    python3 tools/og-preview.py          # rodar da raiz do repositorio

A Baloo 2 (a mesma dos titulos do site) e baixada do Google Fonts na primeira
vez e fica em tools/fonts/, que nao vai para o repositorio.

Isto NAO faz parte do site. O site continua sendo um HTML sem build; este
script so existe para reconstruir a imagem quando a arte ou a foto mudarem.

Ao trocar a imagem por outra, manter as tres regras que o WhatsApp cobra:
JPEG ou PNG (o crawler dele nao renderiza WebP), 1200x630 e abaixo de 300 KB.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, re, sys, urllib.request

AQUI  = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(AQUI, "fonts")
W, H  = 1200, 630

# paleta do site, igual ao :root do index.html
CREAM  = (255, 248, 240)
ORANGE = (250, 116,   1)
WA     = ( 15, 125,  66)
WHITE  = (255, 255, 255)

CSS = "https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800"

def baixa_fontes():
    """Puxa os pesos da Baloo 2 do Google Fonts, uma vez so."""
    os.makedirs(FONTS, exist_ok=True)
    if all(os.path.exists(f"{FONTS}/Baloo2-{p}.ttf") for p in (600, 700, 800)):
        return
    req = urllib.request.Request(CSS, headers={"User-Agent": "Mozilla/5.0"})
    css = urllib.request.urlopen(req).read().decode()
    for peso, url in re.findall(
            r"font-weight:\s*(\d+);.*?src:\s*url\((https://\S+?\.ttf)\)", css, re.S):
        alvo = f"{FONTS}/Baloo2-{peso}.ttf"
        if not os.path.exists(alvo):
            urllib.request.urlretrieve(url, alvo)
            print("baixado", alvo)

def f(peso, tam):
    return ImageFont.truetype(f"{FONTS}/Baloo2-{peso}.ttf", tam)

# ------------------------------------------------------------------ fundo
def fundo(path, offset=0.28):
    """Recorta a foto retrato numa faixa 1200x630, cobrindo sem deformar."""
    im = Image.open(path).convert("RGB")
    sc = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = min(max(int(im.height * offset), 0), im.height - H)
    return im.crop((x, y, x + W, y + H))

def _suave(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def escurecer(im, a0=250, a1=10, ini=0.34, fim=0.86, geral=22):
    """Preto quase solido na esquerda, abrindo para a foto na direita."""
    ramp = Image.new("L", (W, 1))
    p = ramp.load()
    for x in range(W):
        p[x, 0] = round(a0 + (a1 - a0) * _suave((x / W - ini) / (fim - ini)))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, ramp.resize((W, H)))
    # veu geral leve: segura o lado direito para o card nao estourar
    return Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), geral / 255)

# ------------------------------------------------------------------ pecas
def linha(d, xy, trechos, fonte):
    """trechos = [(texto, cor)], desenhados em sequencia na mesma linha."""
    x, y = xy
    for txt, cor in trechos:
        d.text((x, y), txt, font=fonte, fill=cor)
        x += d.textlength(txt, font=fonte)

def pilula(d, x, y, texto, fonte, cor_texto, borda=None, fill=None,
           padx=26, alt=54):
    larg = d.textlength(texto, font=fonte) + padx * 2
    d.rounded_rectangle([x, y, x + larg, y + alt], radius=alt // 2,
                        fill=fill, outline=borda, width=0 if fill else 2)
    cx = fonte.getbbox("Ag")
    d.text((x + padx, y + (alt - (cx[3] - cx[1])) / 2 - cx[1]), texto,
           font=fonte, fill=cor_texto)
    return larg

def badge(lado=104, raio=26):
    """Quadrado arredondado creme com as duas cabecas da logo dentro."""
    cabecas = Image.open("img/logo.png").convert("RGB").crop((90, 84, 326, 264))
    esc = (lado - 14) / max(cabecas.size)
    cabecas = cabecas.resize((round(cabecas.width * esc),
                              round(cabecas.height * esc)), Image.LANCZOS)
    b = Image.new("RGB", (lado, lado), CREAM)
    b.paste(cabecas, ((lado - cabecas.width) // 2, (lado - cabecas.height) // 2))

    m = Image.new("L", (lado * 4, lado * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, lado * 4 - 1, lado * 4 - 1],
                                        radius=raio * 4, fill=255)
    b.putalpha(m.resize((lado, lado), Image.LANCZOS))
    return b

def sombra(camada, desfoque=10, forca=0.62, desce=4):
    """Sombra preta desfocada tirada do proprio recorte da camada de texto."""
    a = camada.getchannel("A").filter(ImageFilter.GaussianBlur(desfoque))
    a = a.point(lambda v: int(v * forca))
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s.putalpha(a)
    fora = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fora.paste(s.crop((0, 0, W, H - desce)), (0, desce))
    return fora

# ------------------------------------------------------------------ card
def card():
    im = escurecer(fundo("img/racao-granel.webp")).convert("RGBA")

    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    X = 62                                       # margem esquerda de tudo

    # cabecalho: nome e onde fica
    xn = X + 104 + 24
    d.text((xn, 44), "AUAUmigão", font=f(800, 60), fill=WHITE)
    d.text((xn + 2, 112), "Bairro Brasília, Cascavel PR", font=f(700, 26),
           fill=ORANGE)

    # manchete: so o que a pagina ja afirma, com o diferencial em laranja
    y, lh = 206, 66
    for tr in ([("Ração a granel de", WHITE)],
               [("mais de 40 marcas", ORANGE), (",", WHITE)],
               [("acessórios, banho e tosa.", WHITE)]):
        linha(d, (X, y), tr, f(800, 57))
        y += lh

    # pilulas dos servicos
    x = X
    for t in ("Banho & Tosa", "Acessórios"):
        x += pilula(d, x, 424, t, f(600, 25), WHITE,
                    borda=(255, 255, 255, 150)) + 14

    # chamada
    pilula(d, X, 506, "Agende no WhatsApp", f(700, 26), WHITE,
           fill=WA, padx=30, alt=58)

    im.alpha_composite(sombra(txt))
    im.alpha_composite(txt)
    im.alpha_composite(badge(), (X, 46))
    return im.convert("RGB")

if __name__ == "__main__":
    baixa_fontes()
    saida = sys.argv[1] if len(sys.argv) > 1 else "img/og-preview.jpg"
    im = card()
    im.save(saida, "JPEG", quality=86, optimize=True, progressive=False)
    kb = os.path.getsize(saida) // 1024
    print(f"{saida}  {im.width}x{im.height}  {kb} KB")
    if kb > 300:
        print("ATENCAO: acima de 300 KB, o WhatsApp pode nao montar o card grande")
