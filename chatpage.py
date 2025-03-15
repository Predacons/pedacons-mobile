from flet import *
import flet.ads as ads
import json
import datetime
from domain_model.chat import Chat


class ChatPage(Control):
    def __init__(self, page: Page, chat: Chat):
        super().__init__(self)
        self.page = page
        self.chat = chat
        self.page.theme.use_material3 = True
        self.page.floating_action_button = FloatingActionButton(
                icon=Icons.EDIT,
                data=0,
                
            )
        self.setup_ui()


    def _get_control_name(self):
        return "container"
    
    def app_bar(self):
        view = AppBar(
            title=Text(self.chat.name),
            leading=IconButton(
                icon=Icons.ARROW_BACK_SHARP,
                on_click=self.go_home
            ),
            actions=[
                IconButton(Icons.MENU, style=ButtonStyle(padding=0), on_click=self.open_settings_page)  # Add on_click event
            ]
        )
        return view
    
    def open_settings_page(self, e):
        self.page.go('/settings')
    
    def setup_ui(self):
        self.page.add(self.app_bar())
        
        # Create a container for the image
        image_container = Container(
            content=Image(src=self.chat.header_image, fit="cover"),
            padding=0,
            width="100%"
        )
        if isinstance(self.chat.metadata, str):
            self.chat.metadata = json.loads(self.chat.metadata)
        # Create a container for the chat details
        details_container = Container(
            content=Column([
                Text(self.chat.name, style="headline4"),
                Text(self.chat.short_description, style="body1"),
                Text(f"Playtime: {self.chat.playtime_forever}", style="body2"),
                Text(f"Last Played: {self.chat.rtime_last_played}", style="body2"),
                Text(f"Completed: {self.chat.completed}", style="body2"),
                Text(f"Completed Date: {self.chat.completed_date}", style="body2"),
                Text(f"Rating: {self.chat.rating}", style="body2"),
                Text(f"Link: {self.chat.link}", style="body2"),
                Text(f"Link2: {self.chat.link2}", style="body2"),
                Text(f"Hide: {self.chat.hide}", style="body2"),
                Text(f"Created Date: {self.chat.createddate}", style="body2"),
                # Additional metadata fields
                Text(f"Type: {self.chat.metadata.get('type', 'N/A')}", style="body2"),
                Text(f"Required Age: {self.chat.metadata.get('required_age', 'N/A')}", style="body2"),
                Text(f"Is Free: {self.chat.metadata.get('is_free', 'N/A')}", style="body2"),
                Text(f"Supported Languages: {self.chat.metadata.get('supported_languages', 'N/A')}", style="body2"),
                Text(f"Reviews: {self.chat.metadata.get('reviews', 'N/A')}", style="body2"),
                Text(f"Website: {self.chat.metadata.get('website', 'N/A')}", style="body2"),
                Text(f"PC Requirements: {self.chat.metadata.get('pc_requirements', 'N/A')}", style="body2"),
                Text(f"Legal Notice: {self.chat.metadata.get('legal_notice', 'N/A')}", style="body2"),
            ]),
            padding=10
        )
        
        # Arrange the image and details in a column
        content_column = ListView([
            image_container,
            details_container
        ],expand=1)
        
        # safe_area = SafeArea(content=content_column)
        self.page.add(content_column)

    def go_home(self, e):
        self.page.go('/')
