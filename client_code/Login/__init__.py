from ._anvil_designer import LoginTemplate
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
@routing.route('login', url_keys=['username'])
class Login(LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    http_get_dict = routing.get_url_dict()
    self.textbox_welcome.text = f"Willkommen Herr/Frau: '{http_get_dict['username']}'"
    self.textbox_username.text = http_get_dict['username']

  def login_button_click(self, **event_args):
    username = self.textbox_username.text
    passwort = self.textbox_passwort.text

    res, msg, user = anvil.server.call("get_user_simple_2", username, passwort)
    if not res or not user or user.get('username', None) == None:
      self.textarea_error.text = msg
    else:
      res, exc, accountno_dict = anvil.server.call("execute_query", f"SELECT accountno FROM users WHERE username = '{username}'")
      res_dict = {'username': username}
      if accountno_dict:
        res_dict['accountno'] = accountno_dict['accountno']
      else:
        res_dict['accountno'] = None
      print(res_dict)
      routing.set_url_hash(url_pattern="users", url_dict=res_dict)

  def logout_clean_url(self):
    anvil.server.call("logout")
    js_window = anvil.js.window
    anvil.server.reset_session()
    js_window.history.replaceState(None, "", js_window.location.pathname)
