from ._anvil_designer import StartpageTemplate
from anvil import *
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
    if state is True:
      open_form('Resultpage', '','', self.check_box_1.checked)
    elif not state and queryparams.get('AccountNo', [None])[0] != None:
      Resultpage = open_form('Resultpage', 'x','x', self.check_box_1.checked, "nologin")
      Resultpage.Label_result.text = "Not Logged in"


  def outlined_button_1_click(self, **event_args):
    username = self.textbox_username.text
    passwort = self.textbox_passwort.text
    secureinput = False
    if self.check_box_1.checked:
      secureinput = True
    anvil.server.call('set_session_secureinput',secureinput)
    anvil.server.call('set_session_accno', anvil.server.call('get_acc_no', username, passwort))
    open_form('Resultpage',username,passwort, secureinput)
    
    