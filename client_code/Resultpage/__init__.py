from ._anvil_designer import ResultpageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.js

class Resultpage(ResultpageTemplate):
  def __init__(self, username, passwort, secureinput, skip=False, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if skip == "nologin":
      print("Not Logged in!")
      return
    try:
      accno = anvil.server.call('loadsessiondata')[0]
    except:
      self.Label_result.text = "Not Logged in!"
      return
    
    secureinput = anvil.server.call('loadsessiondata')[1]
    if secureinput:
      try:
        print(str(accno),str(self.get_query_params()['AccountNo']).strip())
        if str(accno) != str(self.get_query_params()['AccountNo']).strip():
          alert("Nicht verändern!! \n (Man könnte die Veränderung auch einfach ignorieren)")
          self.set_query_params({"AccountNo": accno})
      except:
        ""
    if not skip:
      url = anvil.js.window.location.href
      self.Label_result.text =  anvil.server.call("get_user",username, passwort, url, secureinput)
      print(anvil.server.call('loadsessiondata')[2])
      if anvil.server.call('loadsessiondata')[2] == "valid":
        self.set_query_params({"AccountNo": accno})

    

  def outlined_button_1_click(self, **event_args):
    self.logout_clean_url()
    open_form('Startpage')
    
  def logout_clean_url(self):
    anvil.server.call('logout')
    js_window = anvil.js.window
    anvil.server.reset_session()
    js_window.history.replaceState(None, "", js_window.location.pathname)

  def set_query_params(self, params):
    js_window = anvil.js.window
    current_url = js_window.location.pathname
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    new_url = f"{current_url}?{query_string}"
    js_window.history.replaceState(None, "", new_url)
  def get_query_params(self):
    query_string = anvil.js.window.location.search
    query_params = {}
    if query_string:
        query_string = query_string[1:]  # Remove the "?" from the start
        pairs = query_string.split("&")
        for pair in pairs:
            key, value = pair.split("=")
            query_params[key] = value
    return query_params  # Move this line outside the loop
