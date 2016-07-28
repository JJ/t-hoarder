#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 Mariluz Congosto
# Copyright (C) 2016 modificaciones por JJ Merelo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import os
import re
import sys
import tweepy
import time
import datetime
import codecs
import argparse

class oauth_keys(object):
  def __init__(self,  app_keys_file,user_keys_file):
    self.matrix={}
    self.app_keys_file = app_keys_file
    self.user_keys_file = user_keys_file
    self.app_keys=[]
    self.user_keys=[]
    
    f = open(self.app_keys_file, 'rU')
    for line in f: 
      self.app_keys.append(line.rstrip())
    f.close()
    f = open(self.user_keys_file, 'rU')
    for line in f: 
      self.user_keys.append(line.rstrip())
    f.close()
    return

    
  def get_access(self):
    try: 
      auth = tweepy.OAuthHandler(self.app_keys[0], self.app_keys[1])
      auth.set_access_token(self.user_keys[0], self.user_keys[1])
      api = tweepy.API(auth)
    except:
      print 'Error in oauth autentication, user key ', user_keys_file
      exit(83)
    return api 
 
def get_tweets(api,search_term,regex,how_many):  
  tweets_list=[]
  for tweet in tweepy.Cursor(api.search,
                              q=search_term,
                              rpp=100,
                              result_type="recent",
                              include_entities=True).items(how_many):
    if re.search(regex,tweet.text):
      print tweet.text
  
  return tweets_list

  
def main():

  reload(sys)
  sys.setdefaultencoding('utf-8')
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
  #defino argumentos de script
  parser = argparse.ArgumentParser(description='Search Twitter API REST')
  parser.add_argument('keys_app', type=str, help='file with app keys')
  parser.add_argument('keys_user', type=str, help='file with user keys')
  parser.add_argument('search_term', type=str, help='search term')
  parser.add_argument('regex', type=str, help='regular expression')
  parser.add_argument('how_many', type=int, nargs='?', help='How many tweets',default=1000)

  #obtego los argumentos
  args = parser.parse_args()
  app_keys_file= args.keys_app
  user_keys_file= args.keys_user
  search_term= args.search_term
  regex= args.regex
  how_many = args.how_many
  
  #autenticación con oAuth     
  user_keys= oauth_keys(app_keys_file,user_keys_file)
  api= oauth_keys.get_access(user_keys)

  #Busca
  outpue = get_tweets( api, search_term, regex, how_many)

  #Out
  exit(0)

if __name__ == '__main__':
  main()

