# scrapy_applications

Repo para centralizar aplicacoes que criei usando a lib `scrapy`.

Por enquanto ele contem um unico projeto, que faz o seguinte:
- Faz login no site da CELESC: https://agenciaweb.celesc.com.br/AgenciaWeb/autenticar/autenticar.do
- Seleciona datas de quando quer buscar faturas de energia
- Faz o download das mesmas, e salva na pasta `downloads`

O principal codigo do repo é o `spiders/celesc_post_login.py`, que centraliza praticamente toda a logica de extracao.

Tutoriais que usei: 
- Logando com scrapy: https://www.youtube.com/watch?v=I_vAGDZeg5Q&t=4s
- Baixando arquivos com scrapy: https://coderecode.com/download-files-scrapy/ e tambem https://www.reddit.com/r/scrapy/comments/hh37ur/downloading_images_from_list_of_urls_scrapy_sends/

