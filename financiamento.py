# -*- coding: utf-8 -*- 
"""financiamento.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17MvQz_7oFllYO8chN7nIFijHfUeXqoCS
"""

!pip install pyspark

from pyspark.sql import SparkSession
from pyspark.sql.functions import when, regexp_replace
from pyspark.sql.functions import corr
import pyspark.sql.functions as F
import pandas as pd
import numpy as np
from pyspark.sql.types import IntegerType, FloatType, DoubleType
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from google.cloud import storage

# bucket_name = 'principal'
# file_name = 'operacoes-financiamento-operacoes-indiretas-automaticas'
# client = storage.Client()
# bucket_name = 'economy-squad-7'
# file_name = 'operacoes-financiamento-operacoes-indiretas-automaticas.csv'
# bucket = client.get_bucket(bucket_name)
# blob = bucket.blob(file_name)
# content = blob.download_as_string()

spark = (SparkSession.builder
                    .master('local')
                    .appName('financiamento')
                    .config('financiamento.ui.port', '4050')
                    .getOrCreate()
                    )

df = (spark.read
           .format('csv')
           .option('delimiter', ';')
           .option('header', 'true')
           .option('inferschema', 'true')
           .option('encoding', 'utf-8')
           .option('escape','"')
           .load('/content/drive/MyDrive/Projeto Final/operacoes-financiamento-operacoes-indiretas-automaticas.csv')
           )

df.show()

df.printSchema()

print(f'({df.count()}, {len(df.columns)})')

df.select([F.count(F.when(F.col(c).isNull(), c)).alias(c) for c in df.columns]).show()

df = df.dropna(how='any')

sem_duplicados = df.drop(F.col('cpf_cnpj')).drop_duplicates().count()

qtd_registros = df.count()
total_duplicados = qtd_registros - sem_duplicados
print(total_duplicados)

df = df = df.drop(F.col('cpf_cnpj'), F.col('municipio_codigo'), F.col('cnpj_do_agente_financeiro'),F.col('subsetor_cnae_codigo'))
df = df.drop_duplicates()

print(f'({df.count()}, {len(df.columns)})')

df.select('valor_desembolsado_reais').distinct().orderBy('valor_desembolsado_reais').collect()

df = df.withColumn('valor_desembolsado_reais',
                   F.when(F.col('valor_desembolsado_reais').rlike('^[0-9]+$'),
                          F.col('valor_desembolsado_reais').cast('integer'))
                    .otherwise(F.regexp_replace(F.col('valor_desembolsado_reais'), '[,.]', '').cast('integer')))

df.printSchema()

df.filter(df.valor_desembolsado_reais.isNull()).show()

df = df.dropna(how='any')

df.filter(df.valor_desembolsado_reais.isNull()).show()

df.show(truncate=False)

df.groupBy(F.col('setor_bndes')).count().show()

df.groupBy(F.col('subsetor_bndes')).agg(F.count('*').alias('contagem')).orderBy(F.col('contagem').desc()).show(truncate=False)

df.groupBy(F.col('situacao_da_operacao')).count().show()

df = df.withColumn('juros',
                   F.when(F.col('juros').rlike('^[0-9]+$'),
                          F.col('juros').cast('float'))
                   )

df.select('juros').distinct().orderBy('juros').collect()

df.show(truncate=False)

df.printSchema()

df = df.withColumn("subsetor_bndes", when(df.subsetor_bndes == "OUTRAS", "OUTROS").otherwise(df.subsetor_bndes))

fontes_unicos = df.select('fonte_de_recurso_desembolsos').distinct()

fontes_unicos.orderBy(fontes_unicos["fonte_de_recurso_desembolsos"].desc()).show(truncate=False)

custo_financeiro_unicos = df.select('custo_financeiro').distinct()

custo_financeiro_unicos.orderBy(custo_financeiro_unicos["custo_financeiro"].desc()).show(truncate=False)

modalidade_de_apoio_unicos = df.select('modalidade_de_apoio').distinct()

modalidade_de_apoio_unicos.orderBy(modalidade_de_apoio_unicos["modalidade_de_apoio"].desc()).show(truncate=False)

forma_de_apoio_unicos = df.select('forma_de_apoio').distinct()

forma_de_apoio_unicos.orderBy(forma_de_apoio_unicos["forma_de_apoio"].desc()).show(truncate=False)

#produto

produto_unicos = df.select('produto').distinct()

produto_unicos.orderBy(produto_unicos["produto"].desc()).show(truncate=False)

#instrumento_financeiro

instrumento_financeiro_unicos = df.select('instrumento_financeiro').distinct()

instrumento_financeiro_unicos.orderBy(instrumento_financeiro_unicos["instrumento_financeiro"].desc()).show(truncate=False)

#inovacao

inovacao_unicos = df.select('inovacao').distinct()

inovacao_unicos.orderBy(inovacao_unicos["inovacao"].desc()).show(truncate=False)

#area_operacional

area_operacional_unicos = df.select('area_operacional').distinct()

area_operacional_unicos.orderBy(area_operacional_unicos["area_operacional"].desc()).show(truncate=False)

#setor_cnae

setor_cnae_unicos = df.select('setor_cnae').distinct()

setor_cnae_unicos.orderBy(setor_cnae_unicos["setor_cnae"].desc()).show(truncate=False)

#subsetor_cnae_agrupado

subsetor_cnae_agrupado_unicos = df.select('subsetor_cnae_agrupado').distinct()

subsetor_cnae_agrupado_unicos.orderBy(subsetor_cnae_agrupado_unicos["subsetor_cnae_agrupado"].desc()).show(truncate=False)

#subsetor_cnae_nome

subsetor_cnae_nome_unicos = df.select('subsetor_cnae_nome').distinct()

subsetor_cnae_nome_unicos.orderBy(subsetor_cnae_nome_unicos["subsetor_cnae_nome"].desc()).show((1000), truncate=False)

#porte_do_cliente

porte_do_cliente_unicos = df.select('porte_do_cliente').distinct()

porte_do_cliente_unicos.orderBy(porte_do_cliente_unicos["porte_do_cliente"].desc()).show((1000), truncate=False)

#natureza_do_cliente

natureza_do_cliente_unicos = df.select('natureza_do_cliente').distinct()

natureza_do_cliente_unicos.orderBy(natureza_do_cliente_unicos["natureza_do_cliente"].desc()).show((1000), truncate=False)

#instituicao_financeira_credenciada

instituicao_financeira_credenciada_unicos = df.select('instituicao_financeira_credenciada').distinct()

instituicao_financeira_credenciada_unicos.orderBy(instituicao_financeira_credenciada_unicos["instituicao_financeira_credenciada"].desc()).show((1000), truncate=False)

#situacao_da_operacao

situacao_da_operacao_unicos = df.select('situacao_da_operacao').distinct()

situacao_da_operacao_unicos.orderBy(situacao_da_operacao_unicos["situacao_da_operacao"].desc()).show((1000), truncate=False)

df.show(truncate=False)

df.show()

df = df.withColumn('valor_desembolsado_reais', regexp_replace('valor_desembolsado_reais', r'\d$', ''))