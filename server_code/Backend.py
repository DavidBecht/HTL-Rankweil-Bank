import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3
import urllib.parse
import anvil.js

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
def set_session_accno(accno):
  anvil.server.session["AccountNo"] = accno
@anvil.server.callable
def set_session_secureinput(secureinput):
  anvil.server.session['secureinput'] = secureinput
@anvil.server.callable
def loadsessiondata():
  try:
    return anvil.server.session['AccountNo'], anvil.server.session['secureinput'], anvil.server.session['valid']
  except:
    return anvil.server.session['AccountNo'], anvil.server.session['secureinput']
@anvil.server.callable
def get_user(username, passwort, url, secureinput):
    anvil.server.session['valid'] = 'Temp'
    conn = sqlite3.connect(data_files["database.db"])
    cursor = conn.cursor()
    try:
      # SQL-Abfrage ausführen
      cursor.execute(f"SELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'")
      result = cursor.fetchone()  # Das Ergebnis holen
      cursor.execute("Select AccountNo from Users Where username = ? AND password = ?", (username, passwort))
      result1 = cursor.fetchone()
      queryparams = get_query_params(url)
      accno = queryparams.get('AccountNo', [None])[0]
      if accno != None:
        return get_data_accountno(accno)
      if result:  # Wenn ein Benutzer gefunden wurde
        if result and result1:
          accno = get_acc_no(username,passwort)
          res = get_data_accountno(accno)
        elif not result1 and secureinput:
          anvil.server.session["valid"] = "invalid"
          return f"Login not successful: \nSELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'"
        else:
          res = "Login successful but 'AccountNo' was not passed"
          anvil.server.session["valid"] = "invalid"
        anvil.server.session["login"] = True
        return res  # Serialisierbares Ergebnis zurückgeben
      else:
        anvil.server.session["valid"] = "invalid"
        return f"Login not successful: \nSELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'"  # Klarer Fehlerfall
    except Exception as e:
      return f"Login not successful: {str(e)}"  # Fehlerbeschreibung zurückgeben
    finally:
      conn.close()  # Verbindung schließen
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
  cursor.execute(queryusername)
  user = cursor.fetchone()
  cursor.execute(querybalance)
  balance = cursor.fetchone()
  if balance != None:
    print(anvil.server.session["valid"])
    anvil.server.session["valid"] = "valid"
    return f"Welcome {user}! Your balance is {balance}."
  else:
    return f"User not found \n {querybalance} \n {querybalance}"

    
@anvil.server.callable
def logout():
  anvil.server.session["login"] = False
