from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from controllers.vente_controller import VenteController
from kivy.app import App
from datetime import datetime, timedelta
from models.detail_vente import get_details_par_vente
from models.produits import get_produit
from models.utilisateurs import changer_mot_de_passe

Builder.load_file("kv/parametre_screen.kv")

class ParametreScreen(Screen):
    utilisateur_nom = StringProperty("")
    utilisateur_role = StringProperty("")
    dialog = None

    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        self.utilisateur_nom = app.utilisateur_nom or "-"
        self.utilisateur_role = app.utilisateur_role or "-"

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
        confirm_password = self.ids.confirm_password_input.text
        if not new_password or not confirm_password:
            self.show_dialog("Erreur", "Veuillez remplir les deux champs de mot de passe.")
            return
        if len(new_password) < 6:
            self.show_dialog("Erreur", "Le mot de passe doit contenir au moins 6 caractères.")
            return
        if new_password != confirm_password:
            self.show_dialog("Erreur", "Les mots de passe ne correspondent pas.")
            return
        app = MDApp.get_running_app()
        email = getattr(app, 'utilisateur_email', None)
        if not email:
            self.show_dialog("Erreur", "Impossible de retrouver l'email utilisateur.")
            return
        changer_mot_de_passe(email, new_password)
        self.show_dialog("Succès", "Mot de passe changé avec succès.")
        self.ids.new_password_input.text = ""
        self.ids.confirm_password_input.text = ""

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