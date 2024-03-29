# -*- coding: utf-8 -*- 
"""indice_por_m2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HaTBW_skNTSI5wDSa3OgyrhixcOdZbFZ
"""

pip install gcsfs

pip install pandera

"""##Instalação de bibliotecas"""

import pandas as pd
import os
import numpy as np
from google.cloud import storage
import pandera as pa

"""#Configurando o Google Cloud"""

#CONFIGURANDO DA CHAVE DE SEGURANCA (Enviada com o projeto)

serviceAccount = '/content/squad-7-economia-5ec84694df36.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = serviceAccount

#Configurações Google Cloud Storage
client = storage.Client()
bucket = client.get_bucket('economy-squad-7')
path = 'gs://economy-squad-7/tabelas_filtradas/INDICEm2/indice_m2fipezap.csv'

df = pd.read_csv(path, sep=',', encoding='ISO-8859-1')

"""#Pré-Análise"""

df

#Tam. do DF
df.shape

df.head(5)

df.dtypes

df.count()

"""#Limpeza"""

#Backup local(M.RAM) do df
dfback = df.copy()

df = df.rename(columns={'Unnamed: 1':'UF','VariaÃ§ao mensal MarÃ§_ 2023': 'Variacao_mensal_marco_2023',
                        'VariaÃ§ao mensal Fevereiro_2023':'Variacao_mensal_Fevereiro_2023',
                        'VariaÃ§ao em 2023 (acumulada no ano)':'Variacao_em_2023_(acumulada no ano)',
                        'VariaÃ§ao Anual (ultimas 72 meses)':'Variacao_Anual_(ultimos 72 meses)',
                        'PreÃ§o medio (R$/m2)':'Preco_medio_(R$/m2)'})

df

#Verificando dados nulos, ausentes etc
df.isna().sum()

#regiaocede = df.loc[df['UF'] == 'SP'].groupby('Cidade','UF','Variacao_mensal_marco_2023','Variacao_mensal_Fevereiro_2023','Variacao_Anual_(ultimos 72 meses)','Preco_medio_(R$/m2)')

"""##Enviando para o bucket"""

df.to_csv('indice_m2fipezap_tratado.csv',index=False)

#Carregar direto no bucket
df.to_csv('gs://economy-squad-7/tabelas_filtradas/INDICEm2/indice_m2fipezap.csv',index=False)