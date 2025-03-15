from flet import *
import flet.ads as ads
import json
import datetime
from homepage import MainApp
from settingspage import SettingsPage  # Import SettingsPage
from database import Database
from chatpage import ChatPage

def main(page: Page):
    def Dialog(title,content,lista):

        d=AlertDialog(
            open=False,
            title=Text(title, ),
            content=Text(content, ),
            actions=lista,
            icon=Icon(icons.ERROR_OUTLINE, ),
            icon_padding=padding.only(top=20, bottom=10),
            actions_alignment=MainAxisAlignment.END
        )

        return d
    
    def close_dialog(d):

        global dialog5
        page.close(dialog5)
    
    def Destroy():

        page.window.destroy()


    def BACK(): # For routing with "back" Android button

        global dialog5

        if page.views[-1].route == "/": # Open a exit dialog instead of exit directly (Destroy())

            page.open(dialog5)

        else: # Return to main page if you are not in there

            page.go("/")

    def route_change(route):
        page.clean()
        KEY = ""
        if page.route == '/':
            page.add(MainApp(page))
        elif page.route == '/add':
            page.add(AddPage(page))
        elif page.route.startswith('/chat/'):
            chat_id = int(page.route.split('/')[-1])
            chat = get_chat_by_id(chat_id)
            page.add(ChatPage(page, chat))
        elif page.route == '/settings':  # Add route for settings
            page.add(SettingsPage(page))
    def get_chat_by_id(chat_id):
        db = Database()
        db.connect_to_db()
        chat = db.get_chat_by_id(chat_id)
        db.close_db()
        return chat
    if page.theme is None:
        page.theme = Theme()
    page.theme.use_material3 = True
    page.on_route_change = route_change
    page.go('/')
    dialog5 = Dialog("Exit.", "Want to exit?", [TextButton("No", on_click=lambda _: close_dialog(dialog5)), TextButton("Yes", on_click=lambda _: Destroy())])
    page.window.prevent_close = False # Necesary
    page.on_view_pop = lambda _: BACK() # For routing with "back" Android button

app(target=main)
