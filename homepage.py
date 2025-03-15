from flet import *
import flet.ads as ads
import json
import datetime
from database import Database
from domain_model.chat import Chat
from domain_model.user import User
from chatpage import ChatPage
from typing import List

ENABLE_ADS = True

class MainApp(Control):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme.use_material3 = True
        self.chat_list = ListView(expand=1, spacing=10, padding=20, auto_scroll=False)  # Initialize chat_list as a scrollable Column
        # self.user_id_field = TextField(label="User ID")
        self.page.floating_action_button = FloatingActionButton(
                icon=Icons.ADD,
                data=0,
                on_click=self.open_new_page,
            )
        self.setup_ui()
        # Load chats when the app starts
        self.load_chats(None)
        if ENABLE_ADS and self.page.platform != PagePlatform.WINDOWS:
            self.setup_ads()
    def _get_control_name(self):
        return "container"
    def app_bar(self):
        view = AppBar(
            title=Text("Predacons"),
            actions=[
                IconButton(Icons.MENU, style=ButtonStyle(padding=0), on_click=self.open_settings_page)  # Add on_click event
            ]
        )
        return view

    def open_settings_page(self, e):
        self.page.go('/settings')
        
    def setup_ui(self):
        self.page.add(self.app_bar())
        self.page.add(self.chat_list)
        
    
    def open_new_page(self, e):
        db = Database()
        db.connect_to_db()
        chat = Chat()
        chat_id = db.insert_chat(chat)
        db.close_db()
        self.open_chat_page(chat_id)
    
    def open_chat_page(self,chat_id):
        self.page.go('/chat/'+str(chat_id))

    def load_chats(self, e):

        db = Database()
        db.connect_to_db()
        db_path = db.return_db_path()
        self.page.add(Text(db_path, color="red"))
        chats_data = db.read_chat_db(sort_by="lastupdated DESC")
        db.close_db()
        self.chat_list.controls.clear()
        add_item = ListTile(
            leading=Image(src="https://img.icons8.com/ios/452/plus.png"),
            title=Text("Add new chat"),
            on_click=self.open_new_page
        )
        self.chat_list.controls.append(add_item)
        for chat in chats_data:
            title = chat.title
            vector_db = chat.vectordb
            web_search = chat.websearch
            last_updated = chat.lastupdated
            created_date = chat.createddate
            print(last_updated)
            formatted_last_updated = datetime.datetime.strptime(last_updated.split('.')[0], "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y, %I:%M %p")
            formatted_created_date = datetime.datetime.strptime(created_date.split('.')[0], "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y, %I:%M %p")
            list_item = ListTile(
                title=Text(title),
                subtitle=Text(f"vector db: {vector_db if vector_db else 'No'} \nweb search: {'Yes' if web_search else 'No'} \nlast updated: {formatted_last_updated} \ncreated date: {formatted_created_date}"),
                on_click=lambda _, chat_id=chat.id: self.open_chat_page(chat_id)
            )
            self.chat_list.controls.append(list_item)
    
        self.page.update()

    def setup_ads(self):
        id_banner = (
            "ca-app-pub-3940256099942544/6300978111"
            if self.page.platform == PagePlatform.ANDROID
            else "ca-app-pub-3940256099942544/2934735716"
        )

        self.page.add(
            Container(
                content=ads.BannerAd(
                    unit_id=id_banner,
                    on_click=lambda e: print("BannerAd clicked"),
                    on_load=lambda e: print("BannerAd loaded"),
                    on_error=lambda e: print("BannerAd error", e.data),
                    on_open=lambda e: print("BannerAd opened"),
                    on_close=lambda e: print("BannerAd closed"),
                    on_impression=lambda e: print("BannerAd impression"),
                    on_will_dismiss=lambda e: print("BannerAd will dismiss"),
                ),
                width=320,
                height=50,
                bgcolor=colors.TRANSPARENT,
                alignment=alignment.bottom_center,
            )
        )
