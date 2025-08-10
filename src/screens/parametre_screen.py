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
        old_password = self.ids.old_password_input.text
        new_password = self.ids.new_password_input.text
        confirm_password = self.ids.confirm_password_input.text
        if not old_password or not new_password or not confirm_password:
            self.show_dialog("Erreur", "Veuillez remplir tous les champs.")
            return
        if new_password != confirm_password:
            self.show_dialog("Erreur", "Les mots de passe ne correspondent pas.")
            return
        app = MDApp.get_running_app()
        email = getattr(app, "utilisateur_email", None)
        if not email:
            self.show_dialog("Erreur", "Impossible de récupérer l'email utilisateur.")
            return
        from controllers.utilisateur_controller import UtilisateurController
        from models.utilisateurs import verifier_utlisateur
        utilisateur = verifier_utlisateur(email, old_password)
        if not utilisateur:
            self.show_dialog("Erreur", "Ancien mot de passe incorrect.")
            return
        try:
            UtilisateurController().changer_mot_de_passe(email, new_password)
            self.show_dialog("Succès", "Mot de passe changé avec succès.")
            self.ids.old_password_input.text = ""
            self.ids.new_password_input.text = ""
            self.ids.confirm_password_input.text = ""
        except Exception as e:
            self.show_dialog("Erreur", f"Erreur lors du changement : {str(e)}")

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