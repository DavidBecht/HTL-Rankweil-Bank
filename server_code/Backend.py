import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
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

def get_user_simple(username, password):
  with sqlite3.connect(data_files["database.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = f"SELECT username FROM Users WHERE username = '{username}' AND password = '{password}'"
    try:
      cursor.execute(query)
    except Exception as e:
      return False, f"Login failed!\n\nQuery:\n{query}\n\nError:\n{e}", None
    user = cursor.fetchone()
    if user is None:
      return False, f"Login Failed!\n\nQuery:\n{query}.", None
    return True, "Login Successfull", dict(user)

@anvil.server.callable
def get_user_simple_2(username, password):
  with sqlite3.connect(data_files["database.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = f"SELECT username FROM Users WHERE username = '{username}' AND password = '{password}' AND isActive=1"
    try:
     cursor.execute(query)
    except Exception as e:
      return False, f"Login failed!\n\nQuery:\n{query}\n\nError:\n{e}", None
    user = cursor.fetchone()
    if user is None:
      return False, f"Login Failed!\n\nQuery:\n{query}", None
    return True, "Login Successfull", dict(user)

@anvil.server.callable
def execute_query(query: str, fetchone: bool = True):
  with sqlite3.connect(data_files["database.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
      cursor.execute(query)
    except Exception as e:
      return False, str(e), None
    res = cursor.fetchone() if fetchone else cursor.fetchall()
    if res is None:
      res = {}
    elif fetchone:
      res = dict(res)
    else:
      res = [dict(r) for r in res]
  return True, None, res

@anvil.server.callable
def execute_query_raw(query: str, fetchone: bool = True):
  with sqlite3.connect(data_files["database.db"]) as conn:
    cursor = conn.cursor()
    try:
      cursor.execute(query)
    except Exception as e:
      return False, str(e), None
    res = cursor.fetchone() if fetchone else cursor.fetchall()
  return True, None, res

    
@anvil.server.callable
def logout():
  anvil.server.session["login"] = False
