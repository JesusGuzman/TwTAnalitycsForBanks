from Options import *
from MethodsForTweet import *

if __name__ == "__main__":
  options()
  option = input()
  menu = {1: search_twets,
          2: search_friends,
          3: search_followers}
 
  try:
    select_menu =  menu[option]()
    print  select_menu

  except KeyError:
    print "opcion invalida"
