
#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*

import httplib
import urllib2, urllib
from random import getrandbits
from hashlib import sha1
import json
import hmac
import base64
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
import sys
import facebook
import urlparse
import random
import string
import ast
import mixpanel
import mixpanel_api, json
from mixpanel import Mixpanel
mpTwitter = Mixpanel("070bf8a01a6127ebf78325716490697a")
mpFacebook=Mixpanel("f9177cf864c2778e099d5ec71113d0bf")
mpPinterest=Mixpanel("98b144c253b549db5cdeb812a9323ca3")


network_list = ["twitter", "facebook","googleplus", "pinterest"]
version_list = ["master","latency", "accuracy"]
url_base_remote= "http://metricas-formales.appspot.com/app/refresh_metric"
url_base_local= "http://localhost:8080/refresh_metric"

#de los comandos que ejecuto desde consola, me quedo con el segundo (posicion 1,array empieza en 0),consola: python refresco.py twitter coge la "variable" twitter
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

        #Las credenciales no cambian, a no ser que se quieran hacer peticiones con un usuarios que no sea Deus
        CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
        CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
        ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
        ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret

        listestado=[]
        listtpubl_ms=[]

        #funcion random para crear tweets aleatorios
        def randomword(length):
            return ''.join(random.choice(string.lowercase) for i in range(length))

        estado=randomword(10)
        #PUBLICACION DE TWEET Y REQUEST DEL TIMELINE
        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        request_usertimeline="https://api.twitter.com/1.1/statuses/user_timeline.json"

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_remote + "/Master/twitter-timeline/static/TwitterRefresco.html" + "?" + estado)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_remote + "/Latency/twitter-timeline/static/TwitterRefrescoLatency.html"  + "?" + estado)
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_remote + "/Accuracy/twitter-timeline/static/TwitterRefrescoAccuracy.html" + "?" + estado)
                sleep(3)

   
        #Request publicar tweet
        def publicar(estado):
            if estado == '':
                return 1
            print "--------------------------------------------------------------"
            #CODIGO DE ERROR SI EL TWEET YA ESTABA PUBLICADO (ERROR CODE STATUS 187). CUANDO RESPONSE ==403
            r = requests.post(url=url,data={"status":estado},auth=oauth)
            if r.status_code == 403:
                print "Tweet duplicado"
                return 1
            print "Respuesta: " + str(r)
            tpubl=datetime.datetime.now()
            tpubl_ms=int(time.time()*1000)
            print "tiempo post en ms: " + str(tpubl_ms)
            listestado.append(estado)
            listtpubl_ms.append(tpubl_ms)

            #Request timeline user   
            s= requests.get(request_usertimeline, auth=oauth)
            timeline=s.json()
            #Encontrar el texto del tweet que acabo de publicar, con el campo text que tiene cada tweet, y timestamp cuando me lo muestre en twitter (tambien se puede hacer con ID)(polling)
            for tweet in timeline:
                text=tweet['text']
                if text==estado:
                    break

        #Pruebas
        publicar(estado)

        #zip con todos los post y sus correspondientes tiempos de publicacion
        zipPython=zip(listestado,listtpubl_ms)
        dictPython=dict(zipPython)

        ##########################################################################################################################################
        #-----------------------------------------DATOS TWITTER COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        #pongo 70 segundos porque tengo que esperar a que se produzca el refresco automatico del componente y mande los datos a mixpanel
        sleep(70)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("c10939e3faf2e34b4abb4f0f1594deaa","4a3b46218b0d3865511bc546384b8928")
        lista=[]
        listacomp=[]
        listatime=[]

        if version in version_list:
            if version=="master":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el tweet
                newlist = sorted(lista, key=lambda tweet: tweet['tweet'])

                for y in newlist:
                    #obtengo el texto de cada post recogido del componente
                    textocomp=y.items()[0][1]
                    #obtengo el tiempo de cada post recogido del componente
                    timecomp=y.items()[1][1]
                    #voy guardando ambos datos en dos listas diferentes
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario tweet, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto del tweet y el value son los times de refresco en el componente
                #en la siguiente prueba, aunque en el dict de Python haya dos keys con sus values, dictComp solo tiene una key y un value porque
                #es el nuevo evento. Y busco la key del componente (del nuevo evento) en el dict de Python por lo que siempre va a restar bien los tiempos
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        #resto el tiempo obtenido del componente menos el tiempo que me devuelve directamente la api al postear
                        final_time=int(value)-int(valuesP)
                        print "final_time: " + str(final_time)
                        #mando a Mixpanel el tiempo final obtenido de la resta, el post al que pertenece esa diferencia de tiempo y la version que estamos tratando
                        mpTwitter.track(final_time, "Final time master",{"time final": final_time, "tweet": key, "version":version})

            elif version=="latency":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el tweet
                newlist = sorted(lista, key=lambda tweet: tweet['tweet'])

                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario tweet, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto del tweet y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        final_time=int(value)-int(valuesP)
                        print "final_time: " + str(final_time)
                        mpTwitter.track(final_time, "Final time latency",{"time final": final_time, "tweet": key, "version":version})

            elif version=="accuracy":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el tweet
                newlist = sorted(lista, key=lambda tweet: tweet['tweet'])

                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario tweet, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto del tweet y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        final_time=int(value)-int(valuesP)
                        print "final_time: " + str(final_time)
                        mpTwitter.track(final_time, "Final time accuracy",{"time final": final_time, "tweet": key, "version":"master"})



#--------------------------------------------------
#CASO2: FACEBOOK
#--------------------------------------------------
    elif social_network == 'facebook':

        ##########################################################################################################################################
        #---------------------------------------------------------DATOS FACEBOOK API--------------------------------------------------------------
        ##########################################################################################################################################
        
        #funcion random para crear publicaciones aleatorias
        def randomword(length):
            return ''.join(random.choice(string.lowercase) for i in range(length))

        message=randomword(10)

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/facebook-wall/FacebookRefresco.html" + "?" + message)
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/facebook-wall/FacebookRefrescoLatency.html" + "?" + message)
                sleep(5)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/facebook-wall/FacebookRefrescoAccuracy.html" + "?" + message)
                sleep(5)

        #es necesario cambiar el token cada hora y media: https://developers.facebook.com/tools/explorer/928341650551653 (Get User Access Token, version 2.3)
        access_token='EAANMUmJPs2UBAMhsmC2RmpMyUZCaY8qcB7hnNbCvVhOvcTZB6cPmfyAHNiSP90UoZChLeoAWrHwgZCtaGOubUW3GEZBZBSP5qlqvPrMZBhzmXJtPCDaE5VcPIYA2cZCmZACY3PZAZApfMZCQEHMoyxXGs90vK05L81vDMOTICNuntJLhuwZDZD'

        listestado=[]
        listtpubl_ms=[]

        #uso la API de facebook pasandole como parametro el access token y la version de la api que utilizamos
        graph = facebook.GraphAPI(access_token=access_token, version='2.3')

        #POST EN FACEBOOK
        attachment =  {}
        graph.put_wall_post(message=message, attachment=attachment)
        tpubl=datetime.datetime.now()
        tpubl_ms=int(time.time()*1000)
        print "tiempo post en ms: " + str(tpubl_ms)
        listestado.append(message)
        listtpubl_ms.append(tpubl_ms)

        zipPython=zip(listestado,listtpubl_ms)
        #diccionario con los mensajes publicados y su tiempo de publicacion
        dictPython=dict(zipPython)
        print dictPython

        ##########################################################################################################################################
        #----------------------------------------DATOS FACEBOOK COMPONENTE (RECOGIDOS DE MIXPANEL)-----------------------------------------------
        ##########################################################################################################################################
        #pongo 70 segundos porque tengo que esperar a que se produzca el refresco automatico del componente y mande los datos a mixpanel
        sleep(70)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("1c480cfa1d4cbaaeadc5c102a9ff50ea","b1308de232be2c6edf329081831eba52")
        lista=[]
        listacomp=[]
        listatime=[]

        if version in version_list:
            if version=="master":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=int(value)-int(valuesP)
                            print "final_time: " + str(final_time)
                            mpFacebook.track(final_time, "Final time master",{"time final": final_time, "tweet": key, "version":version})


            elif version=="latency":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=int(value)-int(valuesP)
                            print "final_time: " + str(final_time)
                            mpFacebook.track(final_time, "Final time latency",{"time final": final_time, "tweet": key, "version":version})


            elif version=="accuracy":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=int(value)-int(valuesP)
                            print "final_time: " + str(final_time)
                            mpFacebook.track(final_time, "Final time accuracy",{"time final": final_time, "tweet": key, "version":version})

   


#--------------------------------------------------
#CASO3: GOOGLEPLUS
#--------------------------------------------------
    elif social_network == 'googleplus':

        ##########################################################################################################################################
        #---------------------------------------------------------DATOS FACEBOOK API--------------------------------------------------------------
        ##########################################################################################################################################
        
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/googleplus-timeline/demo/GoogleplusRefresco.html")
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new(url_base_remote + "/Latency/facebook-wall/FacebookRefrescoLatency.html")
                sleep(5)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_remote + "/Accuracy/facebook-wall/FacebookRefrescoAccuracy.html")
                sleep(5)

        

        # import pprint

        # # Set the user's ID to 'me': requires the plus.me scope
        # user_id = 'me'

        # # Insert an Activity
        # print('Insert activity')
        # result = service.activities().insert(
        #     userId = user_id,
        #     body = {
        #         'object': {
        #             'originalContent' : 'Happy Monday! #caseofthemondays'
        #         },
        #         'access': {
        #             'items' : [{
        #                 'type' : 'domain'
        #             }],
        #             'domainRestricted': True
        #         }
        #     }).execute()
        # print('result = %s' % pprint.pformat(result)) 


            

#--------------------------------------------------
#CASO4: PINTEREST
#--------------------------------------------------

    elif social_network == 'pinterest':

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS PINTEREST API---------------------------------------------------------------
        ##########################################################################################################################################
        
        image_url="https://t1.ea.ltmcdn.com/es/images/2/2/0/img_alimentar_cachorros_recien_nacidos_20022_paso_2_600.jpg"

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/pinterest-timeline/demo/PinterestRefresco.html" + "?" + image_url)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/pinterest-timeline/demo/PinterestRefrescoLatency.html" + "?" + image_url)
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/pinterest-timeline/demo/PinterestRefrescoAccuracy.html" + "?" + image_url)
                sleep(3)

        access_token="AXh-Xld9fy7jeDuI23ovntIthRVjFI6N-kmb11xDmW-C0gBCfwAAAAA"
        post_my_board= "https://api.pinterest.com/v1/me/pins/?access_token=" + access_token
        image_url="https://t1.ea.ltmcdn.com/es/images/2/2/0/img_alimentar_cachorros_recien_nacidos_20022_paso_2_600.jpg"
        note="Take a look"
        link="https://www.google.es/search?q=perros&espv=2&biw=1855&bih=966&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjchq_cz8vRAhXCzxQKHQ4DCWMQ_AUIBigB#imgrc=BqLqaxHeCHP0ZM%3A"
        board="829295787572730316"

        listimags=[]
        listtpubl_ms=[]

        def post_pin(access_token, board, note, link, image_url):
            response = urllib.urlopen(
                'https://api.pinterest.com/v1/pins/',
                data=urllib.urlencode(dict(
                    access_token=access_token,
                    board=board,
                    note=note,
                    link=link,
                    image_url=image_url
                )))

            response_data = json.load(response)
            tpubl_ms=int(time.time())
            print "tiempo post en ms: " + str(tpubl_ms)
            listimags.append(image_url)
            listtpubl_ms.append(tpubl_ms)

        post_pin(access_token, board, note, link, image_url)


        zipPython=zip(listimags,listtpubl_ms)
        print zipPython
        #diccionario con los mensajes publicados y su tiempo de publicacion
        dictPython=dict(zipPython)
        print dictPython


        ##########################################################################################################################################
        #----------------------------------------DATOS PINTEREST COMPONENTE (RECOGIDOS DE MIXPANEL)-----------------------------------------------
        ##########################################################################################################################################
        #pongo 70 segundos porque tengo que esperar a que se produzca el refresco automatico del componente y mande los datos a mixpanel
        sleep(70)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales (API KEY y API SECRET)
        x=mixpanel_api.Mixpanel("c6a5d1682613e89df94c6eceb3859be6","17a38edfdff693b56b50f332ae8f8e9e")
        lista=[]
        listacomp=[]
        listatime=[]

        if version in version_list:
            if version=="master":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')
                print respuesta

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=int(value)-int(valuesP)
                            print "final_time: " + str(final_time)
                            mpFacebook.track(final_time, "Final time master",{"time final": final_time, "tweet": key, "version":version})


        