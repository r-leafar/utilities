# utilities
Scripts com utilidade diversas
- [loteToCfe](#loteToCfe)
- [nfeDigV](#nfeDigV)

# loteToCfe
Quando executado faz uma varredura na pasta atual na busca de arquivos [(Xml) de lotes](https://portal.fazenda.sp.gov.br/servicos/sat/Paginas/Guia-Consult-Lote.aspx) de Cfe.
Quando encontrado desmembra eles de maneira que os cupons fiquem salvos de forma separada 
noutra pasta.
<a href="http://www.youtube.com/watch?feature=player_embedded&v=MP8tNBR9Z0Q" target="_blank"><img src="http://img.youtube.com/vi/MP8tNBR9Z0Q/0.jpg" 
alt="Script exemplo" width="240" height="180" border="10" /></a>

# nfeDigV

É um programa de linha de comando que auxilia a encontrar o digito verificador de Nfe´s quando
não se tem a chave completa.

## Opções 
```
usage: nfeDigV.py [-h] [-v] [-m MES] [-ano ANO] chave

positional arguments:
  chave                chave de acesso da Nfe

optional arguments:
  -h, --help           show this help message and exit
  -v, --verbosity      Exibe mais informacoes sobre a chave
  -m MES, --mes MES    Muda o mes para o especificado
  -ano ANO, --ano ANO  Muda o ano para o especificado
```
