import spacy

nlp = spacy.load('pt_core_news_sm')

texto = 'O contrato de locação foi firmado em São Paulo, em 15 de março de 2024.'

doc = nlp(texto.strip())

for token in doc:
    print(f'Token: {token.text:<15}, Lema: {token.lemma_}, POS: {token.pos_}, Stopword: {token.is_stop}')
    
#Propriedades do token
#token.is_stop
#token.is_punct
#token.is_alpha
