from main_imports import MDDialog, MDScreen, MDRaisedButton,BoxLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivymd.uix.button import MDRaisedButton
# from kivymd.uix.dialog import MDDialog
import json as json_
import logging
import requests

from core.config import DEFAULT_PROVIDER
from core.cli.helpers import bannerify, to_stdout
from core.cli.helpers.searcher import link
import threading
from libs.applibs import utils
utils.load_kv("home.kv")

class Loading(BoxLayout):
    pass

class Content(BoxLayout):
    pass

class Home_Screen(MDScreen):
    dialog = None
    call = 0
    def show_confirmation_dialog(self,title_msg):
        print(title_msg,self.call)
        if self.call != 0:
            self.dialog.title = title_msg+" "+"-"+" 125"
            # self.dialog.dismiss()
        self.call = self.call + 1
        if not self.dialog:
            self.dialog = MDDialog(
                title=title_msg+" "+"-"+" 125",
                type="custom",
                content_cls=Content(),
            )
        self.dialog.open()
    def search_result_show(self,text,index):
        # self.ids.rv.data = [] # clear search historic results
        if len(text)>50:
            text = text[:47]+"..."
        self.ids.rv.data.append({"image": "assets\img\profile.jpg","text":text, "index":index})
    def download(self,one,two,name):
        print(one,two)
        self.parent.get_screen("download").download_start(name,40)
        self.dialog.dismiss()
    def call(self,query, json, provider, log_level):
        # Loading()
        # self.parent.bottom("Search in progress Wait !!")
        self.searching()
        threading.Thread(target=self.animdl_search, args=(query, json, provider, log_level,)).start()

    def animdl_search(self, query, json, provider, log_evel):
        print("in ---------")
        # L.ids.Load.active = True
        self.ids.rv.data = []
        logger = logging.getLogger('animdl-searcher')
        session = requests.Session()

        if provider not in link:
            logger.critical(
                "{!r} is not supported at the moment. Selecting the default {!r}.".format(
                    provider, DEFAULT_PROVIDER))
            provider = DEFAULT_PROVIDER

        for i, search_data in enumerate(link.get(provider)(session, query)):
            self.search_result_show(search_data['name'],i)
            self.Search.dismiss()
            # if json:
            #     print(json_.dumps(search_data))
            # else:
            #     logger.info(
            #         '[#{:02d}] {name} \x1b[33m{anime_url}\x1b[39m'.format(
            #             i, **search_data))
    def searching(self):
        if not self.dialog:
            self.Search = MDDialog(
                text="We are searching ....",                
            )
        self.Search.open()