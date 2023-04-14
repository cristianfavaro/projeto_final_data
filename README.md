# Projeto Final 
## Master em Jornalismo de Dados - Insper

Trabalho apresentado na conclusão do módulo Jornalismo de Dados e Automação do Master em Jornalismo de Dados do Insper - turma 2022/23. O projeto foi ministrado pelo professor Eduardo Vicente Gonçalves.  

### O Projeto

A ideia do trabalho surgiu da minha cobertura como setorista de companhias aéreas para o Valor Econômico. Uma dos temas mais presentes no noticiário é o preço da passagem aérea. As tarifas dispararam nos últimos anos por causa dos impactos da pandemia e do efeito da invasão da Rússia na Ucrânia sobre o petróleo. 

A Anac faz um monitoramento intensivo das tarifas, que é disponibilizado em um dashboard interativo bastante eficiente (https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/mercado-do-transporte-aereo), na aba Tarifas Aéreas Domésticas e Tarifas Aéreas Internacionais).

O problema é que eu gostaria de fazer os meus próprios cruzamentos com os microdados e também trabalhar com novas visualizações. 

#### Os Dados

A Anac recolhe das companhias aéreas comerciais uma série de dados mensalmente para calcular a oferta e demanda por transporte, assim como a evolução das tarifas. No caso das tarifas, os dados representam uma fatia de cerca de 35% do total de passageiros transportados (a depender do mês). Esse recorde ocorre, conforme explica a Anac, porque os dados abrangem todas as passagens vendidas ao “público adulto em geral”, excluindo aquelas adquiridas com descontos restritos a grupos específicos, programas de milhagem, entre outras condições. 

As variáveis são diretas:
- ANO e MES: mês e ano da venda das passagens, independentemente da data do voo;
- EMPRESA: (empresa que vendeu a passagem);
- ORIGEM e DESTINO;
- TARIFA (em reais);
- ASSENTOS: por exemplo, uma linha com venda da Azul no mês de janeiro de 2023 por 500 reais com um número de assentos de 9 signifca que, naquele mês a empresa vendeu 9 assentos por 500 reais naquela rota. 

Os microdados estão disponíveis no seguinte link: https://sas.anac.gov.br/sas/downloads/view/frmDownload.aspx

### Ferramentas - Spark

A base completa - janeiro de 2002 a dezembro de 2022 - tem mais de 55 milhões de registros distribuídos em 250 arquivos. Desta forma, abrir o arquivo no Pandas não seria viável na memória do computador. 

Para cruzar os dados, resolvi usar o Pyspark - interface Python para Spark e é um projeto Apache de plataforma cruzada de código aberto. 

### Docker
O Spark é bastante simples de ser iniciado via Docker, método escolhido para este projeto. 
Basta clonar o repositório. Na pasta principal, digite `docker-compose up --build -d` - com isso o Docker vai construir os containeres, iniciar o sistema e manter o terminal livre (detached, ou -d). Ele vai iniciar o Spark, assim como um Worker para processar os dados. 

### Jupyterhttp://localhost:8888/lab
O Docker vai criar também um Jupyter, que pode ser acessado pelo seguinte endereço: http://localhost:8888/
Aqui vai ser possível navegar pela pasta Anac e encontrar os notebooks, assim como os arquivos. 