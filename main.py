#--[Start platform specific code]
"""This code to detect it's Android or not 
if it's not android than app window size change in android phone size"""
from kivy.utils import platform

if platform != 'android':
    from kivy.config import Config
    Config.set("graphics","width",360)
    Config.set("graphics","height",640)
#--[End platform specific code]

#--[Start Soft_Keyboard code ]
"""code for android keyboard. when in android keyboard show textbox   
automatic go to top of keyboard so user can see when he type msg"""
from kivy.core.window import Window

Window.keyboard_anim_args = {"d":.2,"t":"linear"}
Window.softinput_mode = "below_target"
#--[End Soft_Keyboard code ]

from libs.uix.baseclass.home import Home_Screen
from libs.uix.baseclass.downloads import Downloads
from libs.uix.baseclass.root import Root
from main_imports import ImageLeftWidget, MDApp, TwoLineAvatarListItem


class HamsterApp(MDApp):
    """
    Hamster App start from here this class is root of app.
    in kivy (.kv) file when use app.method_name app is start from here
    """

    def __init__(self, **kwargs):
        super(HamsterApp, self).__init__(**kwargs)
        
        self.APP_NAME = "ANIMEDL"
        self.COMPANY_NAME = "Anime.org"
        
    
    def build(self):
        """
        This method call before on_start() method so anything
        that need before start application all other method and code 
        write here.
        """
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "500"

        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.accent_hue = "500"

        self.theme_cls.theme_style = "Light"
    
        self.screen_manager = Root()
        self.screen_manager.add_widget(Home_Screen())
        self.screen_manager.add_widget(Downloads())
        
        return self.screen_manager
    
    
if __name__ == "__main__":
    # Start application from here.
    HamsterApp().run() 
