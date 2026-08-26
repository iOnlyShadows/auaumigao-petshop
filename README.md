# AUAUmigão Petshop

Landing page do AUAUmigão Petshop, Bairro Brasília, Cascavel PR.

## No ar

- **https://ionlyshadows.github.io/auaumigao-petshop/** — design atual
- **https://ionlyshadows.github.io/auaumigao-petshop/novo/** — versão Claymorphism, para comparar

As duas estão com `noindex` e `robots.txt` bloqueando indexação, porque são demonstrações ainda não autorizadas pela loja. **Remover os dois ao publicar no domínio do cliente**, senão o site não aparece no Google.

Site estático de um arquivo. Sem build, sem dependências, sem framework. Para rodar local, basta abrir o `index.html` ou servir a pasta:

```bash
python -m http.server 5173
```

## Estrutura

```
index.html     página inteira, CSS e JS inline
img/           fotos reais da loja e dos clientes
```

## Preview do link no WhatsApp

O card que aparece ao colar o link no WhatsApp sai de `img/og-preview.jpg`, montado a partir da logo e da foto da fachada.

É um JPEG de propósito. O crawler do WhatsApp não renderiza WebP, então enquanto o `og:image` apontava para `img/fachada.webp` o link chegava sem imagem. A fachada também é retrato 765x1020, proporção que o card corta pela metade — por isso a imagem de preview é 1200x630.

Ao trocar essa imagem, manter as três regras: **JPEG ou PNG** (nunca WebP), **1200x630**, **abaixo de 300 KB**. E atualizar `og:image:width` e `og:image:height` junto.

O WhatsApp guarda o preview em cache por URL. Depois de publicar uma mudança, o link antigo continua mostrando o card velho por alguns dias. Para forçar a releitura, passar a URL no [Sharing Debugger do Facebook](https://developers.facebook.com/tools/debug/) e clicar em *Scrape Again*, ou testar com um parâmetro novo no fim (`?v=2`).

## Conteúdo

Tudo na página é verificável. As fotos vieram da fachada da loja e do perfil [@petshop.auaumigao](https://www.instagram.com/petshop.auaumigao/).

A seção de clientes usa os stories reais da loja, com os adesivos que ela mesma colocou. Só foram removidos o cabeçalho e a barra de responder do Instagram. Abrem num visualizador próprio: toque para avançar, segure para pausar, setas do teclado e Escape para sair. O cronômetro não roda para quem pede menos movimento no sistema.

Nenhum depoimento, preço, nota do Google ou forma de pagamento foi inventado. O que não pôde ser confirmado ficou fora da página ou está marcado com `CONFIRMAR` no topo do `index.html`.

## Antes de publicar

Ver o bloco `CONFIRMAR COM O CLIENTE` no início do `index.html`. Em resumo:

1. Confirmar o horário de funcionamento com a loja
2. Confirmar quais serviços de banho e tosa são oferecidos
3. Pegar as coordenadas reais no Google Maps para o JSON-LD
4. Pedir autorização de uso das fotos dos clientes, incluindo os @ que aparecem marcados dentro dos stories
5. Trocar o `canonical`, o `og:url` e o `og:image` pela URL final, nas duas páginas

## Design

Paleta extraída da própria logo da loja: creme `#fff8f0` e laranja `#fa7401`. O laranja da marca reprova contraste como texto (2,64:1 sobre o creme), então aparece só como elemento gráfico. Textos e botões usam tons verificados em WCAG AA, documentados no topo do CSS.

Tipografia: Baloo 2 nos títulos, escolhida por acompanhar o traço arredondado do wordmark da loja. Corpo em fonte de sistema, sem requisição extra.

Motion contido de propósito: o público abre isso em celular popular no 4G. O reveal só roda se o JS estiver vivo, então uma falha de script mostra a página inteira em vez de deixá-la em branco. Tudo respeita `prefers-reduced-motion`.
