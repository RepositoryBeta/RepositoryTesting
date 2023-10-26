import pandas as pd
import seaborn as sns
import numpy as np
import sklearn.preprocessing as pr
datos= pd.read_csv('C:/Users/lisse/Desktop/TESIS/result_train_bert_robert_en.csv')

df=pd.DataFrame(datos)


df['abs_frecuency']=(df['abs_frecuency']-df['abs_frecuency'].min())/(df['abs_frecuency'].max()-df['abs_frecuency'].min())
df['rel_frecuency']=(df['rel_frecuency']-df['rel_frecuency'].min())/(df['rel_frecuency'].max()-df['rel_frecuency'].min())
df['length']=(df['length']-df['length'].min())/(df['length'].max()-df['length'].min())
df['number_syllables']=(df['number_syllables']-df['number_syllables'].min())/(df['number_syllables'].max()-df['number_syllables'].min())
df['token_possition']=(df['token_possition']-df['token_possition'].min())/(df['token_possition'].max()-df['token_possition'].min())
df['number_token_sentences']=(df['number_token_sentences']-df['number_token_sentences'].min())/(df['number_token_sentences'].max()-df['number_token_sentences'].min())
df['number_synonyms']=(df['number_synonyms']-df['number_synonyms'].min())/(df['number_synonyms'].max()-df['number_synonyms'].min())
df['number_hyponyms']=(df['number_hyponyms']-df['number_hyponyms'].min())/(df['number_hyponyms'].max()-df['number_hyponyms'].min())
df['number_hypernyms']=(df['number_hypernyms']-df['number_hypernyms'].min())/(df['number_hypernyms'].max()-df['number_hypernyms'].min())
df['Part_of_speech']=(df['Part_of_speech']-df['Part_of_speech'].min())/(df['Part_of_speech'].max()-df['Part_of_speech'].min())
df['freq_relative_word_before']=(df['freq_relative_word_before']-df['freq_relative_word_before'].min())/(df['freq_relative_word_before'].max()-df['freq_relative_word_before'].min())
df['freq_relative_word_after']=(df['freq_relative_word_after']-df['freq_relative_word_after'].min())/(df['freq_relative_word_after'].max()-df['freq_relative_word_after'].min())
df['len_word_before']=(df['len_word_before']-df['len_word_before'].min())/(df['len_word_before'].max()-df['len_word_before'].min())
df['len_word_after']=(df['len_word_after']-df['len_word_after'].min())/(df['len_word_after'].max()-df['len_word_after'].min())
df['mtld_diversity']=(df['mtld_diversity']-df['mtld_diversity'].min())/(df['mtld_diversity'].max()-df['mtld_diversity'].min())
df['propn']=(df['propn']-df['propn'].min())/(df['propn'].max()-df['propn'].min())
df['aux']=(df['aux']-df['aux'].min())/(df['aux'].max()-df['aux'].min())
df['verb']=(df['verb']-df['verb'].min())/(df['verb'].max()-df['verb'].min())
df['adp']=(df['adp']-df['adp'].min())/(df['adp'].max()-df['adp'].min())
df['noun']=(df['noun']-df['noun'].min())/(df['noun'].max()-df['noun'].min())
df['nn']=(df['nn']-df['nn'].min())/(df['nn'].max()-df['nn'].min())
df['sym']=(df['sym']-df['sym'].min())/(df['sym'].max()-df['sym'].min())
df['num']=(df['num']-df['num'].min())/(df['num'].max()-df['num'].min())
df['avgClsBert']=(df['avgClsBert']-df['avgClsBert'].min())/(df['avgClsBert'].max()-df['avgClsBert'].min())
df['avgTokenBert']=(df['avgTokenBert']-df['avgTokenBert'].min())/(df['avgTokenBert'].max()-df['avgTokenBert'].min())
df['avgSRoBERTa']=(df['avgSRoBERTa']-df['avgSRoBERTa'].min())/(df['avgSRoBERTa'].max()-df['avgSRoBERTa'].min())
df['avgTokenRoBERTa']=(df['avgTokenRoBERTa']-df['avgTokenRoBERTa'].min())/(df['avgTokenRoBERTa'].max()-df['avgTokenRoBERTa'].min())
df.to_csv('C:/Users/lisse/Desktop/TESIS/Norm-ing.csv')















