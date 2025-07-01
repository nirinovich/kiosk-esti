from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from controllers.utilisateur_controller import ajouter_utilisateur

Builder.load_file("kv/register_screen.kv")

class RegisterScreen(Screen):
    def enregistrer_utilisateur(self):
        nom = self.ids.nom_input.text
        email = self.ids.email_input.text
        mot_de_passe = self.ids.mdp_input.text
        role = self.ids.role_input.text

        if nom and email and mot_de_passe and role in ['admin', 'vendeur']:
            ajouter_utilisateur(nom, email, mot_de_passe, role)
            popup = Popup(title="Succès", content=Label(text="Utilisateur enregistré !"),
                          size_hint=(0.6, 0.4))
            popup.open()
            self.manager.current = "login"
        else:
            popup = Popup(title="Erreur", content=Label(text="Champs invalides !"),
                          size_hint=(0.6, 0.4))
            popup.open()
