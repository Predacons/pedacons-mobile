from flet import *
import flet.ads as ads
import json
import datetime
from domain_model.chat import Chat
from domain_model.user import User
from database import Database

class SettingsPage(Control):
    def __init__(self, page: Page):
        super().__init__(self)
        self.page = page
        self.db = Database()
        self.user = None
        self.page.theme.use_material3 = True
        self.page.floating_action_button = FloatingActionButton(
                icon=Icons.SYNC,
                data=0,
                on_click=self.save_user_data
            )
        self.setup_ui()


    def _get_control_name(self):
        return "container"
    
    def app_bar(self):
        view = AppBar(
            title=Text("Settings"),
            leading=IconButton(
                icon=Icons.ARROW_BACK_SHARP,
                on_click=self.go_home
            ),
            actions=[
                IconButton(Icons.CLOSE, style=ButtonStyle(padding=0),on_click=self.go_home)
            ]
        )
        return view
    
    def setup_ui(self):
        self.page.add(self.app_bar())
        self.load_user_data()
        
    def load_user_data(self):
        self.db.connect_to_db()
        users = self.db.read_user_db()
        self.db.close_db()
        if users:
            self.is_new_user = False
            self.user = users[0]  # Assuming single user for simplicity
            self.name_field = TextField(label="Name", value=self.user.name)
            self.vertexapikey_field = TextField(label="Vertex Api Key", value=self.user.vertexapikey)
            self.openaiapikey_field = TextField(label="Openai Api Key", value=self.user.openaiapikey)
            self.azureendpoint_field = TextField(label="Azure Endpoint", value=self.user.azureendpoint)
            self.azureapikey_field = TextField(label="Azure Api Key", value=self.user.azureapikey)
            self.azureapiversion_field = TextField(label="Azure Api Version", value=self.user.azureapiversion)
            self.azuredeploymentname_field = TextField(label="Azure Deployment Name", value=self.user.azuredeploymentname)
            self.maxhistory_field = TextField(label="Maximum History", value=self.user.maxhistory)
            self.metadata_field = TextField(label="Metadata", value=self.user.metadata)
        else:
            self.is_new_user = True
            self.user = User()  # Create a new user instance
            self.name_field = TextField(label="Name")
            self.vertexapikey_field = TextField(label="Vertex Api Key")
            self.openaiapikey_field = TextField(label="Openai Api Key")
            self.azureendpoint_field = TextField(label="Azure Endpoint")
            self.azureapikey_field = TextField(label="Azure Api Key")
            self.azureapiversion_field = TextField(label="Azure Api Version")
            self.azuredeploymentname_field = TextField(label="Azure Deployment Name")
            self.maxhistory_field = TextField(label="Maximum History")
            self.metadata_field = TextField(label="Metadata")
        
        self.page.add(
            SafeArea(
            content=Column([
                self.name_field,
                self.vertexapikey_field,
                self.openaiapikey_field,
                self.azureendpoint_field,
                self.azureapikey_field,
                self.azureapiversion_field,
                self.azuredeploymentname_field,
                self.maxhistory_field,
                self.metadata_field
            ])
            )
        )
        self.page.update()  # Ensure the page is updated after adding components
    
    def save_user_data(self, e):
        if self.user:
            self.user.name = self.name_field.value
            self.user.vertexapikey = self.vertexapikey_field.value
            self.user.openaiapikey = self.openaiapikey_field.value
            self.user.azureendpoint = self.azureendpoint_field.value
            self.user.azureapikey = self.azureapikey_field.value
            self.user.azureapiversion = self.azureapiversion_field.value
            self.user.azuredeploymentname = self.azuredeploymentname_field.value
            self.user.maxhistory = self.maxhistory_field.value
            self.user.metadata = self.metadata_field.value
            self.db.connect_to_db()
            if self.is_new_user:
                self.user.createddate = datetime.datetime.now()
                self.user.lastupdated = datetime.datetime.now()
                self.db.create_user(self.user)
            else:
                self.user.lastupdated = datetime.datetime.now()
                self.db.update_user(self.user)
            self.db.close_db()
            self.page.snack_bar = SnackBar(Text("User data saved successfully!"))
            self.page.snack_bar.open = True
            self.page.update()

    def go_home(self, e):
        self.page.go('/')
