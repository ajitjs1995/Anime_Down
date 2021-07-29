from main_imports import Builder
from kivymd.uix.screen import MDScreen
from libs.applibs import utils

Builder.load_file(r"libs\uix\kv\downloads.kv")


class Downloads(MDScreen):
    def download_start(self,text,value):
        self.ids.rv.data.append({"text":text,"value":value})
        