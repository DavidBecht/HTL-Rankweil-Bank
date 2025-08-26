from ._anvil_designer import UsersTemplate
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
@routing.route("users", url_keys=["username", "accountno"])
class Users(UsersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    http_get_dict = routing.get_url_dict()
    self.username = http_get_dict['username']
    self.accountno = http_get_dict['accountno']
    self.textbox_welcome.text = f"Willkommen Herr/Frau: '{self.username}'"
    query = f"SELECT balance FROM Balances WHERE accountno = {self.accountno}"
    res, exc, balance_dict = anvil.server.call("execute_query", query)
    if not res or not balance_dict or balance_dict.get("balance", None) is None:
      self.textarea_error.text = f"Query:\n{query}\n\nError:\n{exc}"
      balance = 'None'
    else:
      balance = str(balance_dict["balance"])
    row = DataRowPanel(item={'username': self.username, 'accountno': self.accountno, 'balance': balance})
    self.data_grid_balance.add_component(row)

  def login_button_click(self, **event_args):
    username = self.textbox_username.text
    passwort = self.textbox_passwort.text

    res, msg, user = anvil.server.call("get_user_simple_2", username, passwort)
    if not res or not user or user.get("username", None) is None:
      self.textarea_error.text = msg

    else:
      print(user)
      routing.set_url_hash(url_pattern="users", url_dict={})

  def logout_clean_url(self):
    anvil.server.call("logout")
    js_window = anvil.js.window
    anvil.server.reset_session()
    js_window.history.replaceState(None, "", js_window.location.pathname)
