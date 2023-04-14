# Projeto Final 
## Master em Jornalismo de Dados - Insper

### Tarifas aéreas no Brasil: uma análise dos dados da Anac na Ponte Aérea (Rio-SP)

Trabalho apresentado na conclusão do módulo Jornalismo de Dados e Automação do Master em Jornalismo de Dados do Insper - turma 2022/23. O projeto foi ministrado pelo professor Eduardo Vicente Gonçalves. 


### O Projeto
Um dos temas mais presentes na cobertura de um setorista de companhias aéreas é o preço dos bilhetes. As tarifas dispararam nos últimos anos por causa dos impactos da pandemia e do efeito da invasão da Rússia na Ucrânia sobre o petróleo. 

A Anac faz um monitoramento intensivo das tarifas, que é disponibilizado em um dashboard interativo bastante eficiente (https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/mercado-do-transporte-aereo), na aba Tarifas Aéreas Domésticas e Tarifas Aéreas Internacionais). Entretanto, cruzamentos mais espefícos exigem uma demanda formal via assessoria de imprensa e com prazos nem sempre favoráveis. Além disso, ao trabalhar os dados brutos se abrem novas possibilidades de visualizações. 

#### Os Dados
A Anac recolhe das companhias aéreas comerciais uma série de dados mensalmente para calcular a oferta e demanda por transporte, assim como a evolução das tarifas. No caso das tarifas, os dados representam uma fatia de cerca de 35% do total de passageiros transportados (a depender do mês). Esse recorde ocorre, conforme explica a Anac, porque os dados abrangem todas as passagens vendidas ao “público adulto em geral”, excluindo aquelas adquiridas com descontos restritos a grupos específicos, programas de milhagem, entre outras condições. 

As variáveis são diretas:
- ANO e MES: mês e ano da venda das passagens, independentemente da data do voo;
- EMPRESA: empresa que vendeu a passagem;
- ORIGEM e DESTINO;
- TARIFA: valores em reais;
- ASSENTOS: número de passagens comercializadas naquela data pela respectiva tarifa. 

Os microdados estão disponíveis no seguinte link: https://sas.anac.gov.br/sas/downloads/view/frmDownload.aspx

Para facilitar a replicabilidade/teste do projeto, os dados de janeiro de 2002 a dezembro de 2022 estão disponíveis em um arquivo zip no Google Drive (eles devem ser inseridos na pasta 'anac.nosync'): https://drive.google.com/drive/folders/1JYesuNR4Mc5QU2g4gVR9IpoqdUFrrGeq?usp=sharing

### Ferramentas

#### Spark
A base completa - janeiro de 2002 a dezembro de 2022 - tem mais de 55 milhões de registros distribuídos em 250 arquivos. Desta forma, abrir o arquivo no Pandas não seria viável na memória do computador. 

Para cruzar os dados, resolvi usar o Pyspark - interface Python para Spark e é um projeto Apache de plataforma cruzada de código aberto. 

Mas, por uma questão de capacidade de processamento, parte do tratamento dos arquivos foi feita individualmente via Pandas. Após isso, os dados são facilmente agrupados e agregados no Spark. 

#### Docker
O Spark é bastante simples de ser iniciado via Docker, método escolhido para este projeto. 
Basta clonar o repositório. Na pasta principal, digite `docker-compose up --build -d` - com isso o Docker vai construir os containeres, iniciar o sistema e manter o terminal livre (detached, ou -d). Ele vai iniciar o Spark, assim como um Worker para processar os dados. 

#### Jupyter
O Docker vai criar também um Jupyter, que pode ser acessado pelo seguinte endereço: http://localhost:8888/
Aqui é possível navegar pela pasta Anac e encontrar os notebooks necessários para o projeto.  
