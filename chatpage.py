from flet import *
import flet.ads as ads
import json
import datetime
from domain_model.chat import Chat
from google import genai
from google.genai import types


class ChatPage(Control):
    def __init__(self, page: Page, chat: Chat):
        super().__init__(self)
        self.page = page
        self.chat = chat
        self.genai_client = genai.Client(api_key="")
        self.model_id = "gemini-2.0-flash" 
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
            title=Text(self.chat.title),
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
        # image_container = Container(
        #     content=Image(src=self.chat.header_image, fit="cover"),
        #     padding=0,
        #     width="100%"
        # )
        if isinstance(self.chat.metadata, str):
            self.chat.metadata = json.loads(self.chat.metadata)
        # Create a container for the chat details
        details_container = Container(
            content=Column([
                Text(self.chat.title, style="headline4"),
            ]),
            padding=10
        )
        
        # Create a ListView for chat messages
        self.chat_list = ListView(expand=1)
        
        # Create a TextField for user input
        self.input_field = TextField(
            hint_text="Type a message",
            on_submit=self.send_message
        )
        
        # Arrange the image, details, chat messages, and input field in a column
        content_column = Column([
            # image_container,
            details_container,
            self.chat_list,
            self.input_field
        ], expand=1)
        
        self.page.add(content_column)

    def go_home(self, e):
        self.page.go('/')
    def send_message(self, e):
        user_message = self.input_field.value
        if user_message:
            self.chat_list.controls.append(Text(f"You: {user_message}"))
            self.input_field.value = ""
            self.page.update()
            self.get_genai_response(user_message)
    
    def add_message_to_chat(self, message):
        message_container = Container(
            content=Row([
                Text(message),
                IconButton(
                    icon=Icons.COPY,
                    on_click=lambda e: self.copy_to_clipboard(message)
                )
            ])
        )
        self.chat_list.controls.append(message_container)
        self.page.update()
    
    def copy_to_clipboard(self, message):
        self.page.clipboard.set_text(message)
        self.page.snack_bar = SnackBar(Text("Copied to clipboard"))
        self.page.snack_bar.open = True
        self.page.update()

    def display_plain_result(self,response):
        output=''
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                output = output + part.text  # Print text as plain text
            if part.executable_code is not None:
                output = output + part.executable_code.code # Print code as plain text
            if part.code_execution_result is not None:
                output = output + part.code_execution_result.output # Print output as plain text
            if part.inline_data is not None:
                output = output + part.inline_data.data
        return output
    def get_genai_response(self, user_message):
        response = self.genai_client.models.generate_content(
            model=self.model_id,
            contents=user_message,
            config = types.GenerateContentConfig(
                tools=[types.Tool(
                    code_execution=types.ToolCodeExecution
                    )],
                system_instruction="you arw a good person"
                )
            )
        output = self.display_plain_result(response)
        self.chat_list.controls.append(Text(f"Bot: {output}"))
        self.page.update()

