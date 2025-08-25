from ._anvil_designer import UsersTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import routing

@routing.route('users', url_keys=[routing.ANY])
class Users(UsersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    http_get_dict = routing.get_url_dict()

    # Any code you write here will run before the form opens.
