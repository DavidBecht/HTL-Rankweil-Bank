from ._anvil_designer import ResultpageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Resultpage(ResultpageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    print("ADFS")

  def outlined_button_1_click(self, **event_args):
    anvil.server.call('logout')
    open_form('Startpage')
