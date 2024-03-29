# -*- coding: utf-8 -*- 
"""credito_indireto_bndes_filtro.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tJelqRpm-pXUkUlLK77xGhqVmIah9wBC

#Configurações para importação e utilização do Pandas
"""

pip install gcsfs

pip install pandera

import pandas as pd
import os
from google.cloud import storage
import numpy as np
import pandera as pa
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""##Importação do bucket"""

serviceAccount = '/content/squad-7-economia-5ec84694df36.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = serviceAccount
client = storage.Client()
bucket = client.get_bucket('economy-squad-7')
bucket.blob('nao_convencional_tratado.csv')
path = 'gs://economy-squad-7/tratados/nao_convencional_tratado.csv'

df = pd.read_csv(path, sep=',')

"""#Analise inicial

#Verificando a tabela tratada
"""

df

df.shape

print(df.isnull().sum())

df['uf'].unique()

"""##Realizando as filtragens"""

municipios = ['SAO PAULO',
              'ARUJA',
              'BARUERI',
              'BIRITIBA MIRIM',
              'CAIEIRAS',
              'CAJAMAR',
              'CARAPICUIBA',
              'COTIA',
              'DIADEMA',
              'EMBU',
              'FERRAZ DE VASCONCELOS',
              'FRANCISCO MORATO',
              'FRANCO DA ROCHA',
              'GUARAREMA',
              'GUARULHOS',
              'ITAPECERICA DA SERRA',
              'ITAPEVI',
              'ITAQUAQUECETUBA',
              'JANDIRA',
              'JUQUITIBA',
              'MARIPORA',
              'MAUA',
              'MOGI DAS CRUZES',
              'OSASCO',
              'PIRAPORA DO BOM JESUS',
              'POA',
              'RIBEIRAO PIRES',
              'RIO GRANDE DA SERRA',
              'SALESOPOLIS',
              'SANTA ISABEL',
              'SANTANA DO PARNAIBA',
              'SANTO ANDRE',
              'SAO BERNARDO DO CAMPO',
              'SAO CAETANO DO SUL',
              'SAO LOURENCO DA SERRA',
              'SUZANO',
              'TABOAO DA SERRA',
              'VARGEM GRANDE PAULISTA'
              'AGUAS MORNAS',
              'ANTONIO CARLOS',
              'BIGACU',
              'FLORIANOPOLIS',
              'PALHOCA',
              'SANTO AMARO DA IMPERATRIZ',
              'SAO JOSE',
              'SAO PEDRO DE ALCANTARA',
              'GOVERNADOR CELSO RAMOS'
              'ALMIRANTE TAMANDARE',
              'ARAUCARIA',
              'CAMPINA GRANDE DO SUL',
              'CAMPO LARGO',
              'CAMPO MAGRO',
              'COLOMBO',
              'CURITIBA',
              'FAZENDA RIO GRANDE',
              'ITAPERUCU',
              'PINHAIS',
              'PIRAQUARA',
              'QUATRO BARRAS',
              'RIO BRANCO DO SUL',
              'SAO JOSE DOS PINHAIS',
              'ADRIANOPOLIS',
              'BOCAIUVA DO SUL',
              'CERRO AZUL',
              'DOUTOR ULYSSES',
              'ITAPERUCU',
              'RIO BRANCO DO SUL',
              'TUNAS DO PARANA'
              'CARIACICA',
              'FUNDAO',
              'GUARAPARI',
              'SERRA',
              'VIANA',
              'VILA VELHA',
              'VITORIA'
              'BELFORD ROXO',
              'DUQUE DE CAXIA',
              'GUAPIMIRIM',
              'ITABORAI',
              'ITAGUAI',
              'JAPERI',
              'MAGE',
              'MARICA',
              'MESQUITA',
              'NILOPOLIS',
              'NITEROI',
              'NOVA IGACU',
              'PARACAMBI',
              'PETROPOLIS',
              'QUEIMADOS',
              'SEROPEDICA',
              'SAO CONCALO',
              'SAO JOAO DE MERITI',
              'TANGUA',
              'CACHOEIRAS DE MACACU',
              'RIO BONITO',
              'RIO DE JANEIRO']

df = df[df['municipio'].isin(municipios)]

df['uf'].unique()

dfsp = df[df['uf'] == 'SP']
dfsc = df[df['uf'] == 'SC']
dfpr = df[df['uf'] == 'PR']
dfes = df[df['uf'] == 'ES']
dfrj = df[df['uf'] == 'RJ']

csp = dfsp['cliente'].count()
csc = dfsc['cliente'].count()
cpr = dfpr['cliente'].count()
crj = dfrj['cliente'].count()
ces = dfes['cliente'].count()

#Número de habitantes por região metropolitana
nsp = 21900000
nrs = 1209818
npr = 3223836
nrj = 11835708
nvt = 2033067

#Região metropolitana de são paulo tem 21,9 milhões dividiremos por 100 mil para ter o número onde faremos a média
sp = nsp / 100000
contsp = round(csp / sp,2)
print(contsp)

#Regiao metropolitana de Florianopolis tem dividiremos por 100mil para ter o número onde faremos a média
rs = nrs / 100000
contrs = round(csp / rs,2)
print(contrs)

#Regiao metropolitana de Curitiba tem dividiremos por 100mil para ter o número onde faremos a média
pr = npr / 100000
contpr = round(csp / pr,2)
print(contpr)

#Regiao metropolitana do Rio de Janeiro tem dividiremos por 100mil para ter o número onde faremos a média
rj = nrj / 100000
contrj = round(csp / rj,2)
print(contrj)

#Regiao metropolitana de Vitória tem dividiremos por 100mil para ter o número onde faremos a média
vt = nvt / 100000
contvt = round(csp / vt ,2)
print(contvt)

"""##Gerando insights"""

#Municipios que mais tiveram emprestimos cedidos
df.groupby(['municipio','uf'],dropna=False).size().sort_values(ascending=False)

"""##Juros por metropole"""

dfsp['juros'].mean()

dfsc['juros'].mean()

dfpr['juros'].mean()

dfes['juros'].mean()

dfrj['juros'].mean()

"""#Gráficos"""

#Deixando a vizualização da disposição de emprestimos por uf mais fácil
df.groupby(['uf']).size().sort_values(ascending=False).plot.bar(figsize=(10,10))

#Analisando se os juros fornecidos por estado são parecidos
df.plot.scatter(x="juros", y="uf")

#Analisando se o valor do emprestimo influência no juros

juros_contratado = df[['valor_contratado_reais', 'juros']].corr()
sns.heatmap(juros_contratado, annot=True, cmap='coolwarm')

#Analisando se o aumento dos juros de um empréstimo tem relação com o aumento do tempo fornecido de carência

carencia_juros = df[['prazo_carencia_meses', 'juros']].corr()
sns.heatmap(carencia_juros, annot=True, cmap='coolwarm')

"""#Exportando o DF

##Bucket
"""

df.to_csv('gs://economy-squad-7/tabelas_filtradas/bndes_com_consulta_filtrada_UF.csv',index=False)

df_pandas.to_csv('gs://economy-squad-7/tabelas_filtradas/bndes_semconsulta_filtrada_UF.csv',index=False)