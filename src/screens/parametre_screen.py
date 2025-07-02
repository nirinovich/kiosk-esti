from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("kv/parametre_screen.kv")

class ParametreScreen(Screen):
    dialog = None

    def show_dialog(self, title, text):
        box = BoxLayout(orientation='vertical', spacing=10, padding=20)
        box.add_widget(Label(text=text, halign="center"))
        btn = Button(text="OK", size_hint=(1, None), height=40)
        popup = Popup(title=title, content=box, size_hint=(.6, .3), auto_dismiss=False)
        btn.bind(on_release=popup.dismiss)
        box.add_widget(btn)
        popup.open()

    def changer_mot_de_passe(self):
        new_password = self.ids.new_password_input.text
        if not new_password:
            self.show_dialog("Erreur", "Veuillez entrer un nouveau mot de passe.")
            return
        # Ici, ajoute la logique réelle de changement de mot de passe
        self.show_dialog("Succès", "Mot de passe changé (simulation).")
        self.ids.new_password_input.text = ""

    def toggle_theme(self):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"
        self.show_dialog("Info", f"Thème actuel : {app.theme_cls.theme_style}")

    def basculer_theme(self):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"