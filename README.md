# AUAUmigão Petshop

Landing page do AUAUmigão Petshop, Bairro Brasília, Cascavel PR.

Site estático de um arquivo. Sem build, sem dependências, sem framework. Para rodar local, basta abrir o `index.html` ou servir a pasta:

```bash
python -m http.server 5173
```

## Estrutura

```
index.html     página inteira, CSS e JS inline
img/           fotos reais da loja e dos clientes
```

## Conteúdo

Tudo na página é verificável. As fotos vieram da fachada da loja e do perfil [@petshop.auaumigao](https://www.instagram.com/petshop.auaumigao/). Os cães da galeria são clientes reais publicados pela própria loja nos stories.

Nenhum depoimento, preço, nota do Google ou forma de pagamento foi inventado. O que não pôde ser confirmado ficou fora da página ou está marcado com `CONFIRMAR` no topo do `index.html`.

## Antes de publicar

Ver o bloco `CONFIRMAR COM O CLIENTE` no início do `index.html`. Em resumo:

1. Confirmar o horário de funcionamento com a loja
2. Confirmar quais serviços de banho e tosa são oferecidos
3. Pegar as coordenadas reais no Google Maps para o JSON-LD
4. Pedir autorização de uso das fotos dos clientes
5. Trocar o `canonical` e o `og:image` pela URL final

## Design

Paleta extraída da própria logo da loja: creme `#fff8f0` e laranja `#fa7401`. O laranja da marca reprova contraste como texto (2,64:1 sobre o creme), então aparece só como elemento gráfico. Textos e botões usam tons verificados em WCAG AA, documentados no topo do CSS.

Tipografia: Baloo 2 nos títulos, escolhida por acompanhar o traço arredondado do wordmark da loja. Corpo em fonte de sistema, sem requisição extra.

Motion contido de propósito: o público abre isso em celular popular no 4G. O reveal só roda se o JS estiver vivo, então uma falha de script mostra a página inteira em vez de deixá-la em branco. Tudo respeita `prefers-reduced-motion`.
