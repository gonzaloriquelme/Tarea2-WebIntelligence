# -*- coding: 850 -*-
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import gensim
import math
#r.iloc[1] #acceso a la fila 1
#r['rel'] #acceso a la columna rel
#
#se procede a leer los datos
print "Leyendo CSV"
r = pd.read_csv('relation10.csv', sep = ';')
#u = pd.read_csv('users10.csv', sep = ';') los leeremos despues para que no ocupen memoria en la primera parte
#t = pd.read_csv('tweets10.csv', sep = ';')
#se trabaja la base de datos eliminando las filas con NA's

r=r.dropna(axis=0, how='any')
#print r.count, con esto se ve que quedan 98737 observaciones


#Se crea el grafo
print "Generando Grafo"
G = nx.Graph()

#Por temas de procesamiento se trabajar  solo con el 5% de los datos, los cuales seran seleccionados tomando un n£mero al azar
#y todas las observaciones sucesivas hasta completar un 5%, esto pues de realizarlo al azar, existiendo usuarios con mas de una fila de relaciones
#podria inducir a perder parte de las relaciones de ese usuario, lo que se evita al tomar un segmento
x=random.randint(0,math.floor(98736*0.95))
print x

#las pruebas se haran con el x seleccionado al azar como numero fijo para un entendimiento mas acabado de las tareas que se realizan
y=int(x+math.floor(98736*0.05))


#A continuaci¢n se seleccionan los usuarios y sus respectivas relaciones (los que pasaran a ser nodos)
#Se distingue a los distintos usuarios dentro de la columna relaci¢n por medio de los espacios
#y finalmente se forman las aristas entre los nodos
for i in range(x,y):
  a=r['user_id'].iloc[i]
  G.add_node(a)
  v=r['rel'].iloc[i].split(' ')
  for j in range(0,len(v)):
     G.add_edge(a,v[j])


#Se dibuja y muestra el grafo resultante de estas relaciones
print "Dibujando Grafo"
nx.draw(G)
plt.show()

#Se realiza el pagerank
print "Calculando PageRank"
pr = nx.pagerank(G)

#Se desea buscar los 20 ids con pageranks mas altos y mas bajos
altos=sorted(pr, key=pr.get)[-20:]
bajos=sorted(pr, key=pr.get)[:20]

print altos
print bajos

#a es momento de leer los datos de los usuarios para comparar los followers con el pagerank encontrado
u = pd.read_csv('users10.csv', sep = ';')

print "Obteniendo numero de followers"
#se crean dos vectores para ser llenados y graficados mas adelante
followers = []
page_rank = []
#En pr, key vendria siendo el user_id y value el pagerank obtenido para cada user
#se completan los vectores por medio de las id encontradas en pr
for key,value in pr.iteritems():
    lista_twit = u.index[u['twitter_id']==int(key)].tolist()
    if (len(lista_twit) > 0):
        id = lista_twit[0]
        n_followers = u['followerscount'].get(id)
        followers.append(n_followers)
        page_rank.append(value)
        #print("user: ", key)
        #print("followers: ", n_followers)
        #print("ranking: ", value)



#se compara los pagerank obtenidos con la popularidad por medio de un gr fico de dispersi¢n
print "Graficando Followers vs PageRank"
plt.scatter(followers, page_rank)
plt.show()


t = pd.read_csv('tweets10.csv', sep = ';')

n_tweets = t.groupby('user_id').count()
print n_tweets

print "RTW calculation"

RTW = []
RT=0

M = []
M1=0

idx = 0 # es el indice que va apuntando a cada usuario de la tabla u
# i es el nombre de usuario (con el que se hace mencion)
for i in u['screename']:
    # Para cada usuario se reinicia el contador de RT y Menciones
    RT = 0
    M1 = 0
    print ('Buscando: @' + str(u['screename'][idx]))
    # j es el mensaje completo
    for j in t['text']:
        # Buscamos solamente el @screename
        if (('@'+str(u['screename'][idx])) in j):
            print "Encontrado username"
            # Luego si esta con 'rt @' al lado, entonces es RT
            if ('rt @' + str(u['screename'][idx])) in j:
                RT = RT + 1
            # Si no esta con 'rt @', entonces es Mencion
            else:
                M1 = M1 + 1
    RTW.append(RT)
    M.append(M1)

    idx = idx + 1

    # descomentar para que se detenga en el usuario nro 20
    #if idx == 20:
    #    break

idx = 0 # es el indice que va apuntando a cada usuario de la tabla u
for i in u['screename']:
    user_id = str(u['twitter_id'][idx]) # twitter_id
    name = str(u['screename'][idx])     # screename
    rtw = str(RTW[idx])
    m = str(M[idx])
    print('User_id: ' +user_id + '\t;  RT: ' + rtw + '\t;  M: ' + m + '\t;  Screename: ' + name)
    idx = idx + 1
