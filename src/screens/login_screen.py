from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from controllers.utilisateur_controller import verifier_connexion

Builder.load_file("kv/login_screen.kv")

class LoginScreen(Screen):
    def se_connecter(self):
        email = self.ids.email_input.text
        mot_de_passe = self.ids.mdp_input.text

        utilisateur = verifier_connexion(email, mot_de_passe)

        if utilisateur:
            role = utilisateur[4]  
            app = App.get_running_app()
            app.utilisateur_role = role
            app.utilisateur_id = utilisateur[0]  # Stocke l'id utilisateur
            app.ajouter_ecrans_utilisateur()  # Recrée les écrans avec le bon id
            app.ajouter_vente_screen_utilisateur()  # Recrée l'écran vente avec le bon id
            self.manager.current = "home" 
        else:
            popup = Popup(title="Erreur de connexion",
                          content=Label(text="Email ou mot de passe incorrect"),
                          size_hint=(0.6, 0.4))
            popup.open()
