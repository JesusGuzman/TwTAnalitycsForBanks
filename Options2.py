from MethodsForTweet import *
from beautifultable import BeautifulTable
from dateutil.parser import parse
from pyfiglet import Figlet
import io
import json

from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import time
import dateutil

#global word_global

twitter_api = oauth_login()

def options():
  table = BeautifulTable()
  f = Figlet(font='slant')
  print f.renderText('saxsa')
  table.column_headers = ["OPCION", "FUNCIONALIDAD"]
  table.append_row([ 1  , "Buscar Tweets" ])
  table.append_row([ 2  , "Encontrar Amigos" ])
  table.append_row([ 3  , "Encontrar Seguidores" ])
  print table
  print "ingrese en numero que desea: "

def get_user_twett(results_json):
  parsed_json = json.loads(results_json)
  table = BeautifulTable()
  table.column_headers = ["USUARIO", "TWTTEO LO SIGUIENTE", "created"]
  for key in parsed_json:
    user = key['user']['screen_name']
    text = key['text']
    created = key['created_at']
    dt = parse(created)
    date = dt.strftime('%d/%m/%Y')
    table.append_row([user.encode('utf-8'), text.encode('utf-8'), date])
  
  table.sort('created')
  print table
  grafica_veces(list (table['created']))

def options_brands():
  table = BeautifulTable()
  table.column_headers = ["Opcion", "Aseguradora"]
  table.append_row([ 1  , "Seguros Monterrey " ])
  table.append_row([ 2  , "El Aguila Compania de Seguros" ])
  table.append_row([ 3  , "GNP Seguros" ])
  print table
  print "ingrese en numero que desea: "

def search_twets():
  #print "ingresa palabra: "
  options_brands()
  entrada = input()  
  if entrada == 1 :
    word = "seguros monterrey"
  elif entrada == 2 :
    word = "seguros el aguila"
  else :
    word = "gnp seguros"


  #word = input()
  global word_global
  word_global = word
  results = twitter_search(twitter_api, word, max_results= 1000 )
  save_json(word, results)
  results_json = load_json(word)
  get_user_twett(results_json)

def search_friends():
  print "ingrese nombre: "
  screen_word  = input()
  f_ids, fo_ids = get_friends_followers_ids(twitter_api,
                                    screen_name= screen_word,
                                    friends_limit=1000,
                                    followers_limit=10000)
  get_friends_profile(twitter_api, user_ids=f_ids)


def search_followers():
  print "ingrese nombre: "
  screen_word  = input()
  f_ids, fo_ids = get_friends_followers_ids(twitter_api,
                                    screen_name= screen_word,
                                    friends_limit=1000,
                                    followers_limit=10)
  get_followers_profile(twitter_api, user_ids=fo_ids)

def grafica_veces(dates):
  tmp_dates = list(set(dates))
  tmp_dates.sort()
  global frecuence_global
  global dates_global
  frecuence = [ ]
  for date in tmp_dates :
    #print "para:  " + date + " aparece: " + str(dates.count(date))
    frecuence.append(dates.count(date))
  frecuence_global = frecuence
  dates_global = tmp_dates
  botche(tmp_dates, frecuence)

def botche(x , y):
  days = [ ]
  for key in x :
    array_tmp = key.split("/")
    days.append(int(array_tmp[0]))
  plt.plot(days,y)
  plt.xlabel('dia')
  plt.ylabel('frecuencia')
  plt.title('Frecuencia de Tweets')
  plt.savefig('books_read.png')
  plt.close()

  create_pdf()

def average_tweets():
  frecuence = frecuence_global
  average = 0
  for key in frecuence :
    average = int(average) + int(key)
  average_final = average/len(frecuence)
  return average_final

def max_frecuence():
  frecuence = frecuence_global
  return max(frecuence)

def min_frecuence():
  frecuence = frecuence_global
  return min(frecuence)

def max_frecuence_date() :
  dates = dates_global
  frecuence = frecuence_global
  max_frecuence = max(frecuence)
  index = frecuence.index(max_frecuence)
  return dates[index]
  
def min_frecuence_date() :
  dates = dates_global
  frecuence = frecuence_global
  max_frecuence = min(frecuence)
  index = frecuence.index(max_frecuence)
  return dates[index]

def first_date():
  dates = dates_global
  return dates[0]
  
def last_date():
  dates = dates_global
  [parse(x) for x in dates]
  sorted(dates)
  return dates[len(dates)-1]

def create_pdf():
  date = time.strftime("%x")
  brand = word_global
  
  if brand == "seguros monterrey" :
    image = "log-aseg-65.png"
  elif brand == "seguros el aguila" :
    image = "log-aseg-17.png"
  elif brand == "gnp seguros" :
    image = "log-aseg-24.png"

  c = canvas.Canvas("prueba.pdf")
  c.drawImage(image,350,755,230,75)
  c.drawString(30,740,'EXTRACCION Y ANALISIS DE CONTENIDOS DIGITALES')
  c.drawString(30,715,'Fuente de extraccion: Twitter')
  c.drawString(500,740,date)

  c.drawString(340,715,'Concepto:')
  c.drawString(440,715, brand)

  c.drawString(30,695,'Reporte:')
  c.drawString(120,695,"Frecuencia de Tweets al dia que hablan sobre " + brand)
  c.drawImage("books_read.png",50,400,250,250)
 
  c.drawImage("saxsa.jpg",20,750,150,75)

  c.drawString(290,610,'Promedio de Twetts al dia: ' + str(average_tweets()))
  c.drawString(290,590,'Dia con mayor frecuencia: ' + max_frecuence_date())
  c.drawString(290,570,'Dia con menor frecuencia: ' + min_frecuence_date())
  c.drawString(290,550,'Frecuencia mas alta: ' + str(max_frecuence()))
  c.drawString(290,530,'Frecuencia mas baja: ' + str(min_frecuence()))
  c.drawString(290,490,'Total de Tweets: ' + str(min_frecuence()))
  
  c.showPage()
  c.save()


