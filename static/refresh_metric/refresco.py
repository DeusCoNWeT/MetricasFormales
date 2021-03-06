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
mpGithub=Mixpanel("870ae6fd08343fcfb154ad6ed5227c47")
mpPinterest=Mixpanel("98b144c253b549db5cdeb812a9323ca3")


##########################################################################################################################################
##########################################################################################################################################
#----------------------------------------------------------------OAUTH 1.0----------------------------------------------------------------
##########################################################################################################################################
##########################################################################################################################################

CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret

class OauthTwitter():

  def __init__(self, consumer_key, consumer_secret, access_key, access_secret):

    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.access_key = access_key
    self.access_secret = access_secret
    self.request_url ="https://api.twitter.com/oauth/request_token"
    self.authenticate_url = "https://api.twitter.com/oauth/authenticate"
    self.request_usertimeline="https://api.twitter.com/1.1/statuses/user_timeline.json"

  def get_auth_token(self):

    #Crear todos los parametros que se necesitan y meterlos en la cabecera. Los parametros viene especificados por la API de Twitter
    HEADER_TITLE = "Authorization"
    #Consumer key
    HEADER = 'OAuth oauth_consumer_key="' + self.consumer_key + '", '
    #Nonce
    nonce= str(getrandbits(64))
    HEADER += 'oauth_nonce="' + nonce +'", '
    #Timestamp
    timestamp= str(int(time.time()))
    #Signature
    key= urllib2.quote(self.consumer_secret) + "&" + urllib2.quote (self.access_secret)

    # Join all of the params together
    #params_str = "&".join(["%s=%s" % (encode(k), encode(HEADER[k])) for k in sorted(HEADER)])

    base_string = 'GET&' + urllib2.quote(self.request_url, safe="") + '&' + urllib2.quote("oauth_consumer_key=" + self.consumer_key + "&oauth_nonce=" + nonce +
        "&oauth_signature_method=HMAC-SHA1&oauth_timestamp=" + timestamp + "&oauth_token=" + self.access_key +"&oauth_version=1.0",safe="")

    #md5.digest()
    signature= hmac.new(key,base_string, sha1).digest()
    #para pasar a ascii necesito un codificador (base64)
    signature = base64.standard_b64encode (signature).decode('ascii')
    HEADER += 'oauth_signature="' + urllib2.quote(signature, safe="") + '", '

    #Signature Method
    HEADER += 'oauth_signature_method="HMAC-SHA1", '
    #Timestamp
    HEADER += 'oauth_timestamp="' + timestamp + '", '
    #TOKEn
    HEADER += 'oauth_token="' + self.access_key + '", '
    #Version
    HEADER += 'oauth_version="1.0"'

    #Peticion de token, devuelve oauth_token,oauth_token_secret y oauth_callback_confirmed
    req= urllib2.Request(self.request_url)
    req.add_header(HEADER_TITLE, HEADER)
    response = urllib2.urlopen(req).read()
    response = [k.split("=") for k in response.split("&")]
    #response_json = {}
    #for k in response:
      #response_json[k[0]] = k[1]

    tokens=[]
    for v in response:
        token1=v[1]
        tokens.append(token1)
    oauth_token=tokens[0]
    oauth_token_secret=tokens[1]
    oauth_verifier1=tokens[2]

#-------------------------------------------------------------------------------------------------------------------
#Get Authorization URL. Request para permitir autorizacion
    # authoriza= "https://api.twitter.com/oauth/authorize?oauth_token=%s" % oauth_token
    # req1=urllib2.Request(authoriza)
    # response1 = urllib2.urlopen(req1).read()
    # webbrowser.open(authoriza)
    # time.sleep(3)

    # oauth_verifier="TnEti5JqFtKcQqVxFtcLMrcpyPrRyuuy"
    # access_token_url= "https://api.twitter.com/oauth/access_token?oauth_verifier=%s" % oauth_verifier

#Request token y token secret finales
    # req5= urllib2.Request(access_token_url)
    # req5.add_header(HEADER_TITLE, HEADER)
    # response5 = urllib2.urlopen(req5).read()

#     oauth = OAuth1Session(self.consumer_key,self.consumer_secret,oauth_token,oauth_token_secret,oauth_verifier)
#     oauth_tokens = oauth.fetch_access_token(self.access_token_url)
#     resource_owner_key = oauth_tokens.get('oauth_token')
#     resource_owner_secret = oauth_tokens.get('oauth_token_secret')

#---------------------------------------
#Get Authentication URL.
    #authorize_url1 = self.authenticate_url +'?'+"oauth_token=" + oauth_token
    #authent = "https://api.twitter.com/oauth/authenticate?oauth_token=%s" % oauth_token
    #req2=urllib2.Request(authent)
    #response2=urllib2.urlopen(req2).read()
   #mirar como sacar los parametros de la url al hacer esta peticion. O ver donde me devuelve el oauth_token y el oauth_verifier
    #webbrowser.open(authent)
#-----------------------------------------

#PRUEBAS
objeto = OauthTwitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
respuesta = objeto.get_auth_token()





##########################################################################################################################################
##########################################################################################################################################
#------------------------------------------------------------METRICA REFRESCO-------------------------------------------------------------
##########################################################################################################################################
##########################################################################################################################################


network_list = ["twitter", "facebook", "github","pinterest"]
version_list = ["master","latency", "accuracy"]

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
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Master/twitter-timeline/static/TwitterRefresco.html" + "?" + estado)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Latency/twitter-timeline/static/TwitterRefrescoLatency.html"  + "?" + estado)
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Accuracy/twitter-timeline/static/TwitterRefrescoAccuracy.html" + "?" + estado)
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
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Master/facebook-wall/FacebookRefresco.html" + "?" + message)
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Latency/facebook-wall/FacebookRefrescoLatency.html" + "?" + message)
                sleep(5)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Accuracy/facebook-wall/FacebookRefrescoAccuracy.html" + "?" + message)
                sleep(5)

        #es necesario cambiar el token cada hora y media: https://developers.facebook.com/tools/explorer/928341650551653 (Get User Access Token, version 2.3)
        access_token='EAACEdEose0cBAE5bEFEuNzQr4Iv7Dlc4NXdi9oUZAJZAv7Xniepo5TZAkf30I3LHgwDG7sJNszCoCHR8uIc9iTsNebX7LOlXknSUZCohAHfzvkJxDisy0VJZAQQ49Yy7DfZC9RbfvzxwEvvlKqMdyLEPyZCGduZAQ7e8JOG53fiZAZAQZDZD'

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
#CASO3: GITHUB
#--------------------------------------------------

    elif social_network == 'github':

        ##########################################################################################################################################
        #----------------------------------------------------------DATOS GITHUB API---------------------------------------------------------------
        ##########################################################################################################################################
        payload ="Found a new bug"
        listestado=[]
        listtpubl_ms=[]
        
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Master/github-events/GithubRefresco.html"  + "?" + payload)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Latency/github-events/GithubRefrescoLatency.html"  + "?" + payload)
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Accuracy/github-events/GithubRefrescoAccuracy.html"  + "?" + payload)
                sleep(3)

        #se ha de cambiar el token: https://github.com/settings/tokens
        headers = {'Authorization': 'token dda3ad66696''f12542b7b14a2372c6f9f4225ca71' }

        #funcion crear un repositorio
        def post_repo():
            url='https://api.github.com/user/repos'
            payload = {'name': 'sandraguapa2', 'auto_init': True, 'private':False, 'gitignore_template': 'nanoc'}
            r = requests.post(url=url,data=json.dumps(payload),headers=headers)

        #funcion crear una issue
        def post_issue():
            url='https://api.github.com/repos/sandragyaguez/prueba/issues'
            payload = { "title": "Found a new bug","body": "I'm having a problem with this."}
            r = requests.post(url=url,data=json.dumps(payload),headers=headers)
            #print r.status_code
            #print r.text

        #funcion crear una pull request
        def post_pullrequest():
            url='https://api.github.com/repos/sandragyaguez/prueba/pulls'
            payload = { "title": "Amazing new feature","body": "Please pull this in!","head": "rama_prueba","base": "master"}
            r = requests.post(url=url,data=json.dumps(payload),headers=headers)
        
        post_issue()
        tpubl=datetime.datetime.now()
        tpubl_ms=int(time.time()*1000)
        print "tiempo post en ms: " + str(tpubl_ms)
        listestado.append(payload)
        listtpubl_ms.append(tpubl_ms)

        #zip con mensaje posteado y el tiemnpo de publicacion
        zipPython=zip(listestado,listtpubl_ms)
        dictPython=dict(zipPython)
        print dictPython


        ##########################################################################################################################################
        #-------------------------------------------DATOS GITHUB COMPONENTE (RECOGIDOS DE MIXPANEL)-----------------------------------------------
        ###########################################################################################################################################


        sleep(70)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("4fe88dd4a1adad7b14889b4e7da2c204","e38bfa81176f69b094dd41ad1f28292c")
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
                newlist = sorted(lista, key=lambda tweet: tweet['tweet'])

                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        final_time=int(value)-int(valuesP)
                        print "final_time: " + str(final_time)
                        mpGithub.track(final_time, "Final time master",{"time final": final_time, "tweet": key, "version":version})


            elif version=="latency":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda tweet: tweet['tweet'])

                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        final_time=int(value)-int(valuesP)
                        print "final_time: " + str(final_time)
                        mpGithub.track(final_time, "Final time latency",{"time final": final_time, "tweet": key, "version":version})

            elif version=="accuracy":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda tweet: tweet['tweet'])

                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        final_time=int(value)-int(valuesP)
                        print "final_time: " + str(final_time)
                        mpGithub.track(final_time, "Final time accuracy",{"time final": final_time, "tweet": key, "version":version})


#--------------------------------------------------
#CASO4: PINTEREST
#--------------------------------------------------

    elif social_network == 'pinterest':

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS PINTEREST API---------------------------------------------------------------
        ##########################################################################################################################################
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://localhost:8080/refresh_metric/Master/pinterest-timeline/demo/PinterestCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://localhost:8080/refresh_metric/Latency/pinterest-timeline/demo/PinterestCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://localhost:8080/refresh_metric/Accuracy/pinterest-timeline/demo/PinterestCompletitudAccuracy.html")
                sleep(3)

        access_token="AXh-Xld9fy7jeDuI23ovntIthRVjFI6N-kmb11xDmW-C0gBCfwAAAAA"
        post_my_board= "https://api.pinterest.com/v1/me/pins/?access_token=" + access_token
        image_url="https://www.pinterest.com/pin/687643436823691338/"
        note="Take a look, it is GitHub"
        link="https://www.pinterest.com/r/pin/687643436823691338/4779055074072594921/3cdbba8c79c29eba41db0a63e1b7ea42ff8a705745fc44e54f86ec42ecd50874"
        #"id": "687643436823691338"}
        board="Tablero 1"
        #url="https://api.pinterest.com/v1/boards/anapinskywalker/wanderlust/pins/?"
        #r = requests.post(url=post_my_board,data={"status":"https://www.google.es/search?q=imagen+perro&espv=2&biw=1855&bih=966&tbm=isch&imgil=BUZ0QjOy-024-M%253A%253BIFiRlwaSmIYu2M%253Bhttp%25253A%25252F%25252Fwww.todoperros.com%25252F&source=iu&pf=m&fir=BUZ0QjOy-024-M%253A%252CIFiRlwaSmIYu2M%252C_&usg=__1xfgSCfQ9SeDEmHfz-5d5zzLjvs%3D&ved=0ahUKEwi6rYvu6ubQAhUCvBQKHT9gDRYQyjcIMw&ei=Tn5KWLrOBIL4Ur_AtbAB#imgrc=BUZ0QjOy-024-M%3A"})
        #print r


        def post_pin(access_token, board, note, link, image_url):
            response = urllib2.urlopen(
                'https://api.pinterest.com/v1/pins/',
                data=urllib2.urlencode(dict(
                    access_token=access_token,
                    board=board,
                    note=note,
                    link=link,
                    image_url=image_url,
                )))
            response_data = json.load(response)
            return response_data

        print post_pin(access_token, board, note, link, image_url)
