import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3
import urllib.parse

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
@anvil.server.callable
def get_login_state():
  if "login" not in anvil.server.session:
    anvil.server.session["login"] = False
  return anvil.server.session["login"]
@anvil.server.callable
def get_user(username, passwort, url):
  conn = sqlite3.connect(data_files["database.db"])
  cursor =  conn.cursor()
  try:
      res = (cursor.execute(f"SELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'"))
      result = cursor.fetchone()
      queryparams = get_query_params(url)
      accno = queryparams.get('AccountNo', [None])[0]
      if result:
        res = get_data_accountno(accno)
        anvil.server.session["login"] = True
  except Exception:
      res = f"Login not successful: \n {res}'"
  return res
@anvil.server.callable
def get_acc_no(username, passwort):
  conn = sqlite3.connect(data_files["database.db"])
  cursor =  conn.cursor()
  res = (cursor.execute(f"SELECT AccountNo FROM Users WHERE username = '{username}' AND password = '{passwort}'"))
  res = cursor.fetchone()
  try:
    return res[0]
  except: 
    return None
@anvil.server.callable
def get_query_params(url):
  query = url.split('?')[-1] if '?' in url else ''
  query = urllib.parse.parse_qs(query)
  return query
  
@anvil.server.callable
def get_data_accountno(accountno):
  conn = sqlite3.connect(data_files["database.db"])
  cursor = conn.cursor()
  querybalance = f"SELECT balance FROM Balances WHERE AccountNo = {accountno}"
  queryusername = f"SELECT username FROM Users WHERE AccountNo = {accountno}"
  try:
    user = list(cursor.execute(queryusername))
    balance = list(cursor.execute(querybalance))
    if accountno != None:
      return f"Welcome {user}! Your balance is {balance}."
    else:
      return "Login successful but AccountNo was not passed"
    
  except:
    return ""
    
@anvil.server.callable
def logout():
  anvil.server.session["login"] = False
