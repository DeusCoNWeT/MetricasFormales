#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib2, urllib
import json
import time
from time import sleep
from twitter import *
from requests_oauthlib import OAuth1
import requests
import webbrowser
import urllib3
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import datetime
import re
import ast
import calendar
import mixpanel
import os
from mixpanel import Mixpanel
mp = Mixpanel("10b73632200abfbd592a5567ae99f065")
mpGithub=Mixpanel("6dbce2a15a7e5bbd608908e8d0ed8518")
import mixpanel_api


#JFS
#CONSUMER_KEY= "7pBOCbidtVpQfTpPpwvQBL31o"
#CONSUMER_SECRET = "0M3o2TTQQQi4fqXx03XRkfUIOXZBa3sIN0w5q7culXPnVv3enb"
#ACCESS_KEY = "249717000-nG3UUpnfHkhIkyhnA8KpClgVKK0Uc2kl33qTrBdP"
#ACCESS_SECRET = "erdkRUxv9eKGjfNHSkpzxi0kUYGAlOvI7ESOdPuxEv4OA"

#---------------------------------------------------------------------------------------------------------------------
#def main():
network_list = ["twitter","instagram", "facebook", "github"]
version_list = ["master","latency", "accuracy"]
server_base_url = "http://localhost:8000"

#de los comandos que ejecuto desde consola, me quedo con el segundo (posicion 1,array empieza en 0),consola: python completitud.py twitter coge la "variable" twitter
if len(sys.argv) >= 2:
    social_network = sys.argv[1]
else:
    social_network = ''

if len(sys.argv) >= 3:
    version= sys.argv[2]
else:
    version = ''

#CASOS:
if social_network in network_list:

#--------------------------------------------------
#CASO1: TWITTER
#--------------------------------------------------

    if social_network == 'twitter':

        ##########################################################################################################################################
        #---------------------------------------------------------DATOS TWITTER API---------------------------------------------------------------
        ##########################################################################################################################################

        CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
        CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
        ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
        ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret
        # Lanzamos una pestana por cada version del componente

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/TwitterCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/TwitterCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/TwitterCompletitudAccuracy.html")
                sleep(3)

        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        request_hometimeline="https://api.twitter.com/1.1/statuses/home_timeline.json?count=200"
        #Request timeline home
        s= requests.get(request_hometimeline, auth=oauth)
        timeline=s.json()
        contador=0
        lis=[]
        ids=[]
        for tweet in timeline:
            #if para ver si el tweet es un retweet
            if(tweet.has_key('retweeted_status')):
                text = tweet['retweeted_status']['text']
            else:
                text=tweet['text']

            id_tweet1=tweet['id_str']
            id_tweet1=int(id_tweet1)
            user=tweet['user']['name']
            contador=contador+1
            lis.append(text)
            #Twitter devuelve los id de los tweets cronologicamente (comprobado)
            ids.append(id_tweet1)
        print contador
        zipPython=zip(ids,lis)
        dictPython=dict(zipPython)

        ##########################################################################################################################################
        #-----------------------------------------DATOS TWITTER COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        sleep(10)
                # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("0be846115003ba87c667ee6467edb336","c282259a64f150a4ce2496a2dd73e097")
        lista=[]
        listacomp=[]
        listaid=[]
        cont=0

        if version in version_list:
            if version=="master":
                #defino los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda id_tweet: id_tweet['id'])
                newlist.reverse()

                for y in newlist:
                    #la k son los text y el id y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    textocomp=y.items()[0][1]
                    idcomp=y.items()[1][1]
                    idcomp=int(idcomp)
                    listacomp.append(textocomp)
                    listaid.append(idcomp)
                
                zipComp=zip(listaid,listacomp)
                dictComp=dict(zipComp)

                #Recorro el diccionario del componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        cont+=1
                        valuesP=dictPython.get(key,None)
                        if cmp(valuesP,value)==0:
                            print "OK"
                            cont+=1
                        else:
                            print "falla en: " + value
                            cont+=1
                            mp.track(cont,"Fallos accuracy",{"posicion": cont , "tweet": value, "version":version})

                    else:
                        print "falla en: " + str(key)
                        print "el tweet es: " + value
                        cont+=1
                        mp.track(cont,"Fallos master",{"posicion": cont , "tweet": value, "version":version})

                    
            elif version=="latency":
                        #defino los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                            #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                        #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda id_tweet: id_tweet['id'])
                newlist.reverse()

                for y in newlist:
                        #la k son los text y el id y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    textocomp=y.items()[0][1]
                    idcomp=y.items()[1][1]
                    idcomp=int(idcomp)
                    listacomp.append(textocomp)
                    listaid.append(idcomp)

                zipComp=zip(listaid,listacomp)
                dictComp=dict(zipComp)

                #Recorro el diccionario del componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        cont+=1
                        valuesP=dictPython.get(key,None)
                        if cmp(valuesP,value)==0:
                            print "OK"
                            cont+=1
                        else:
                            print "falla en: " + value
                            cont+=1
                            mp.track(cont,"Fallos accuracy",{"posicion": cont , "tweet": value, "version":version})
                    else:
                        print "falla en: " + str(key)
                        print "el tweet es: " + value
                        cont+=1
                        mp.track(cont,"Fallos latency",{"posicion": cont , "tweet": value, "version":version})


            elif version=="accuracy":
                             #defino los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                            #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                        #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda id_tweet: id_tweet['id'])
                newlist.reverse()

                for y in newlist:
                        #la k son los text y el id y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    textocomp=y.items()[0][1]
                    idcomp=y.items()[1][1]
                    idcomp=int(idcomp)
                    listacomp.append(textocomp)
                    listaid.append(idcomp)

                zipComp=zip(listaid,listacomp)
                dictComp=dict(zipComp)

                #Recorro el diccionario del componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        if cmp(valuesP,value)==0:
                            print "OK"
                            cont+=1
                        else:
                            print "falla en: " + value
                            cont+=1
                            print cont
                            mp.track(cont,"Fallos accuracy",{"posicion":cont ,"tweet": value, "version":version})

                    else:
                        print "falla en: " + str(key)
                        print "el tweet es: " + value
                        cont+=1
                        mp.track(cont,"Fallos accuracy",{"posicion": cont, "tweet": value, "version":version})



#--------------------------------------------------
#CASO1: GITHUB
#--------------------------------------------------
                
    elif social_network == 'github':

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://localhost:8080/GithubCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://localhost:8080/GithubCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://localhost:8080/GithubCompletitudAccuracy.html")
                sleep(3)

        ##########################################################################################################################################
        #----------------------------------------------------------DATOS GITHUB API---------------------------------------------------------------
        ##########################################################################################################################################

        github_url = "https://api.github.com/users/mortega5/received_events"
        peticion= requests.get(github_url)
        print peticion
        muro=peticion.json()
        for events in muro:
            print events
            print "------------------------------------------------------------------"
            #idsevents=events['id']
            #print idsevents




        ##########################################################################################################################################
        #------------------------------------------DATOS GITHUB COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        sleep(10)
                # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("1119893e7fea6aad13e030ad514595be","bf69f1d1620ca5a5bb2b116c3e3a9944")

        if version in version_list:
            if version=="master":
                #defino los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')               
                    
            elif version=="latency":
                        #defino los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')
                

            elif version=="accuracy":
                             #defino los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

    
    #elif social_network == 'facebook' and len(sys.argv) >= 3:
        #     access_token = sys.argv[2]
            
    
    #else:
        #print "Wrong social network or missing param"
        # {}: Obligatorio, []: opcional
        #print "Usage: completitud.py {twitter|facebook|instagram|github [facebook_access_token]"


#if __name__ == "__main__":
    #main()

