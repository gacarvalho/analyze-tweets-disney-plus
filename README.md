![Sobre: Título do projeto](https://github.com/gacarvalho/analyze-tweets-disney-plus/blob/main/background-project/background-TITLE-img.png?raw=true)

## 📌 PROPOSTA DO PROJETO

O principal objetivo do projeto é desenvolver um crawler para capturar os tweets em tempo real sobre o 'novo serviço' de streaming da Disney : Disney Plus. Após a realização da captação dos tweets na ferramenta Twitter era necessário implementar uma pipeline automatizando com a ferramenta Pentaho (PDI) para limpeza, organização e estruturação dos dados. Posteriormente, escrever os dados limpos e tratados em uma tabela relacional : DataLake : MySQL. 

📢  ETAPA : EXTRAÇÃO 

Para a realização da extração dos tweets foi necessário utilizar a linguagem Python e a utilização da API do Twitter, transformando as colunas e extraindo para um DataLake : MySQL.

```bash
# EXTRAÇÃO DOS DADOS : DISNEY PLUS
$ !pip install tweepy datetime

# CAPTURANDO OS TWEETS EM TEMPO REAL
$ !python3 get_tweets.py

# ESTRUTURA JSON
$ !python3 get_tweets.py

# Importando as bibliotecas necessárias
$ import json

$ with open('collected_tweets_2021-03-13-21-41-21.txt','r', encoding="utf-8") as file:
    tweets = file.readlines()

# Parse dos tweets
$ parsed_tweets = [json.loads(json.loads(i)) for i in tweets]

# Quantos tweets foram capturados?
$ len(parsed_tweets)

# ACESSANDO AS CHAVES DO JSON : DICIONÁRIO

$ primeiro_tweet = parsed_tweets[0]

$ primeiro_tweet['user']

# TRANSFORMANDO OS TWEETS EM UMA ESTRUTURA ANALISÁVEL

# Importando as Bibiliotecas necessárias
$ import pandas as pd

$ with open('collected_tweets_2021-03-13-21-41-21.txt','r', encoding="utf-8") as file:
    tweets = file.readlines()
    
$ with open('tweet.json','w') as f:
    json.dump(
        json.loads(json.loads(tweets[0])), f
    )
    
# Parse dos tweets

$ parsed_tweets = [json.loads(json.loads(i)) for i in tweets]

# Quantos tweets foram capturados : restante
$ len(parsed_tweets)

# ACESSANDO AS CHAVES DO JSON : DICIONÁRIO

$ primeiro_tweet = parsed_tweets[0]

$ primeiro_tweet['user']

# TRANSFORMANDO OS TWEETS EM UMA ESTRUTURA ANALISÁVEL

$ df_tratado = pd.DataFrame(primeiro_tweet).reset_index(drop=True).iloc[:1]

# Verificando o df_tratado
$ df_tratado

# Verificando as colunas do df_tratado
$ df_tratado.columns

# Deletando as colunas de df_tratado
$ df_tratado.drop(columns=['quote_count', 'reply_count', 'retweet_count','favorite_count',
'favorited', 'retweeted', 'user', 'entities', 'quoted_status', 'quoted_status_permalink', 'extended_tweet', 'possibly_sensitive', 'quoted_status_id', 'quoted_status_id_str'], errors='ignore', inplace=True)

# Modificando os nomes da colunas 
$ df_tratado['user_id'] = primeiro_tweet['user']['id']
$ df_tratado['user_id_str'] = primeiro_tweet['user']['id_str']
$ df_tratado['user_screen_name'] = primeiro_tweet['user']['screen_name']
$ df_tratado['user_location'] = primeiro_tweet['user']['location']
$ df_tratado['user_description'] = primeiro_tweet['user']['description']
$ df_tratado['user_protected'] = primeiro_tweet['user']['protected']
$ df_tratado['user_verified'] = primeiro_tweet['user']['verified']
$ df_tratado['user_followers_count'] = primeiro_tweet['user']['followers_count']
$ df_tratado['user_created_at'] = primeiro_tweet['user']['created_at']

# Exibindo o primeiro tweet e as suas informações
$ df_tratado

# Trabalhando com as entidades : MENÇÕES

$ user_mentions = []

$ for i in range(len(primeiro_tweet['entities']['user_mentions'])):
    dicionariobase = primeiro_tweet['entities']['user_mentions'][i].copy()
    dicionariobase.pop('indices',None)
    df = pd.DataFrame(dicionariobase, index=[0])
    df = df.rename(columns={'screen_name': 'entities_screen_name',
    'name':'entities_name',
    'id':'entities_id',
    'id_str':'entities_id_str'})
    user_mentions.append(df)

$ user_mentions[0]

$ dfs = []

$ for i in user_mentions:
    dfs.append(
        pd.concat([df_tratado.copy(),i], axis=1)
    )

$ pd.concat(dfs, ignore_index=True)

# FUNÇÃO : TRATAMENTO DO TWEET E CONVERTE EM DATAFRAME PANDAS


$ def tweet_para_df(tweet):
    try:
        # criação do Data Frame do Tweet
        df_tratado = pd.DataFrame(tweet).reset_index(drop=True).iloc[:1]

        # retirada das colunas que não serão utulizadas
        df_tratado.drop(columns=['quote_count', 'reply_count', 'retweet_count','favorite_count','favorited', 'retweeted', 
        'user', 'entities' 'quoted_status', 'quoted_status_permalink', 'extended_tweet', 'possibly_sensitive', 
        'quoted_status_id', 'quoted_status_id_str'], errors='ignore', inplace=True)

        #inclusão das colunas com os dados do user
        df_tratado['user_id'] = tweet['user']['id']
        df_tratado['user_id_str'] = tweet['user']['id_str']
        df_tratado['user_screen_name'] = tweet['user']['screen_name']
        df_tratado['user_location'] = tweet['user']['location']
        df_tratado['user_description'] = tweet['user']['description']
        df_tratado['user_protected'] = tweet['user']['protected']
        df_tratado['user_verified'] = tweet['user']['verified']
        df_tratado['user_followers_count'] = tweet['user']['followers_count']
        df_tratado['user_created_at'] = tweet['user']['created_at']

        #inclusão das colunas com os dados do user_mentions
        user_mentions = []
        for i in range(len(tweet['entities']['user_mentions'])):
            dicionariobase = tweet['entities']['user_mentions'][i].copy()
            dicionariobase.pop('indices',None)
            df = pd.DataFrame(dicionariobase, index=[0])
            df = df.rename(columns={'screen_name': 'entities_screen_name',
            'name':'entities_name',
            'id':'entities_id',
            'id_str':'entities_id_str'
            })
            user_mentions.append(df)
        # junção das linhas user_mentions
        dfs = []
        for i in user_mentions:
            dfs.append(
                pd.concat([df_tratado.copy(),i], axis=1)
            )
        df_final = pd.concat(dfs, ignore_index=True)
    except:
        return None
    return df_final

# PADRONIZANDO OS TWEETS

$ %%time
$ parseados = [tweet_para_df(tweet) for tweet in parsed_tweets]

# Eliminando as posições vazias da lista
$ parseados = [i for i in parseados if i is not None]

$ tratado = pd.concat(parseados, ignore_index=True)

# Consultando 'tratado'
$ tratado

# INGESTÃO DE DADOS DO TWEETER NO MYSQL

$ !pip install pymysql

# Importando as bibliotecas necessárias 
$ import sqlalchemy
$ import pymysql

# Conexão com a base de dados : MySQL
$ engine = sqlalchemy.create_engine(f"mysql+pymysql://root:oli@am@localhost/dbDisneyPlus?charset=utf8mb4")

$ tratado.to_sql("tweets_disney",con=engine, index=True, if_exists='append')
```

## 🎲 Tratamento de dados / Processo ETL na ferramenta Pentaho (PDI)

Na transformação dos dados foi necessário utilizar a ferramenta Pentaho. O primeiro passo foi necessário capturar os dados em um DataLake : MySQL, logo após foi essencial realizar a transformação, deletando algumas colunas, complementando campos vazios, ordenando os dados e extraindo para um Data Mart. 

![Tratamento de dados](https://github.com/gacarvalho/analyze-tweets-disney-plus/blob/main/etl/transformation.gif?raw=true)

Logo após o desenvolvimento do tratamento dos dados foi necessário automatizar esse processo, e para isso, foi aplicado um JOB. 

![Tratamento de dados](https://github.com/gacarvalho/analyze-tweets-disney-plus/blob/main/etl/transformation.gif?raw=true)



