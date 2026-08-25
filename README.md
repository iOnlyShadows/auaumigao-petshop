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

Tudo na página é verificável. As fotos vieram da fachada da loja e do perfil [@petshop.auaumigao](https://www.instagram.com/petshop.auaumigao/).

A seção de clientes usa os stories reais da loja, com os adesivos que ela mesma colocou. Só foram removidos o cabeçalho e a barra de responder do Instagram. Abrem num visualizador próprio: toque para avançar, segure para pausar, setas do teclado e Escape para sair. O cronômetro não roda para quem pede menos movimento no sistema.

Nenhum depoimento, preço, nota do Google ou forma de pagamento foi inventado. O que não pôde ser confirmado ficou fora da página ou está marcado com `CONFIRMAR` no topo do `index.html`.

## Antes de publicar

Ver o bloco `CONFIRMAR COM O CLIENTE` no início do `index.html`. Em resumo:

1. Confirmar o horário de funcionamento com a loja
2. Confirmar quais serviços de banho e tosa são oferecidos
3. Pegar as coordenadas reais no Google Maps para o JSON-LD
4. Pedir autorização de uso das fotos dos clientes, incluindo os @ que aparecem marcados dentro dos stories
5. Trocar o `canonical` e o `og:image` pela URL final

## Design

Estilo **Claymorphism** (variante web), escolhido pela skill ui-ux-pro-max a partir de "pet shop local business grooming warm friendly". Superfícies macias e tácteis: borda de 3px, raio grande, sombra dupla com aresta sólida embaixo, e o elemento afundando até a aresta ao ser pressionado. É a aresta que faz parecer objeto, não a sombra difusa.

Paleta ainda vem da logo da loja (creme , laranja ). A skill sugeriu  como cor primária e  como azul de confiança. Medi os dois: o laranja reprova como texto (2,64:1) e até com branco por cima (2,8:1), então segue sendo apenas gráfico, como o próprio checklist da skill exige (mínimo 4,5:1). O azul passa nos dois sentidos e entrou, restrito à faixa de dados de contato.

Tipografia: **Varela Round** nos títulos e **Nunito Sans** no corpo, o par que a skill recomenda para produtos pet.

Escala de raio em três níveis: superfície 28px, cartão 22px, botão 16px. Círculo só em avatar e anel de story.

Área de toque de todos os 30 elementos interativos chega a 44px. Nos links de texto isso é feito com pseudo-elemento, para não inchar o layout.

Motion contido de propósito: o público abre isso em celular popular no 4G. Micro-interações em 160 a 180ms com curva de mola. O reveal só roda se o JS estiver vivo, então uma falha de script mostra a página inteira em vez de deixá-la em branco. Tudo respeita `prefers-reduced-motion`.
