from ._anvil_designer import StartpageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from anvil.tables import app_tables
from anvil_extras import routing

@routing.default_template
@routing.route('')

class Startpage(StartpageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def login_button_click(self, **event_args):
    username = self.textbox_username.text
    password = self.textbox_passwort.text
    res, msg, user =  anvil.server.call("get_user_simple",username, password)
    query = f"SELECT username FROM Users WHERE username = '{username}'"
    res, exc, _user = anvil.server.call("execute_query_raw", query)
    query = f"SELECT password FROM Users WHERE password = '{password}'"
    res, exc, _password = anvil.server.call("execute_query_raw", query)
    print(_user)
    print(_password)
    if not res or not user or user.get('username', None) == None:
      self.textarea_error.text = msg
    elif _user is not None and len(_user) > 0 and username == _user[0] and _password is not None and len(_password) > 0 and password == _password[0]:
      query = f"SELECT accountno FROM Users WHERE username = '{username}'"
      res, exc, _accno = anvil.server.call("execute_query_raw", query)
      routing.set_url_hash(url_pattern="users", url_dict={'username': _user[0], 'accountno': _accno[0]})
    else:
      routing.set_url_hash(url_pattern='login', url_dict={'username': self.textbox_username.text})
      
  def logout_clean_url(self):
    anvil.server.call('logout')
    js_window = anvil.js.window
    anvil.server.reset_session()
    js_window.history.replaceState(None, "", js_window.location.pathname)
    
    