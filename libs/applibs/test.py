from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

KV = '''
<Content> 
    MDSpinner:
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': .5, 'center_y': .5}
        active: True 

        palette:
            [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],             [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],             [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],[0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],


MDFloatLayout:

    MDFlatButton:
        text: "ALERT DIALOG"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_confirmation_dialog()
'''


class Content(BoxLayout):
    pass


class Example(MDApp):
    dialog = None

    def build(self):
        return Builder.load_string(KV)

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
               
                type="custom",
                content_cls=Content(),
                
            )
        self.dialog.open()


Example().run()





    