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

class Startpage(StartpageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    url = anvil.js.window.location.href
    queryparams = anvil.server.call('get_query_params', url)
    state = anvil.server.call('get_login_state')
    if not state and queryparams.get('AccountNo', [None])[0] != None:
      Resultpage = open_form('Resultpage', 'x','x', self.check_box_1.checked, "nologin")
      Resultpage.Label_result.text = "Not Logged in"
    if state is True:
      open_form('Resultpage', '','', self.check_box_1.checked)
    else:
      self.logout_clean_url()


  def login_button_click(self, **event_args):
    username = self.textbox_username.text
    passwort = self.textbox_passwort.text
    secureinput = False
    if self.check_box_1.checked:
      secureinput = True
    anvil.server.call('set_session_secureinput',secureinput)
    anvil.server.call('set_session_accno', anvil.server.call('get_acc_no', username, passwort))
    self.Label_result.text =  anvil.server.call("get_user",username, passwort, url, secureinput)
    open_form('Resultpage',username,passwort, secureinput)
  def logout_clean_url(self):
    anvil.server.call('logout')
    js_window = anvil.js.window
    anvil.server.reset_session()
    js_window.history.replaceState(None, "", js_window.location.pathname)
    
    