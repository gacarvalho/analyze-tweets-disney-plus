import json 
from tweepy import OAuthHandler, Stream, StreamListener  #faz requisicao de tweets ao Twitter
from datetime import datetime

# CADASTRAR AS CHAVES DE ACESSO

consumer_key = "YGSFrzszgES6SFMtZTUghUhlw"
consumer_secret = "TITEr8yC97JPTaiG9flVZrGc8INvFkObHpznB6NnupabE3OKx2"

access_token = "1342352348497272833-J2FXw9MGDeiOQFSRLzsyJog94VOiRH"
access_token_secret = "x5pdI1Fos0MMxidVxMYkfq5GrJ2u8GNounFan74SzuRZE"

# DEFININDO UM ARQUIVO DE SAÍDA PARA ARMAZENAR OS TWEETS COLETADOS

data_hoje = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
out = open(f"collected_tweets_{data_hoje}.txt", "w")

# IMPLEMENTAR UM CLASSE PARA CONEXÃO COM TWITTER

class MyListener(StreamListener):

    ## My Listener está recebendo uma herança da classe StreamListener!
    def on_data(self, data):
        itemString = json.dumps(data)
        out.write(itemString + "\n")
        return True 

    def on_error(self, status):
        print(status)   

# IMPLEMENTAR A FUNÇÃO MAIN 

if __name__ == "__main__":
    l = MyListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=["DisneyPlus"])
