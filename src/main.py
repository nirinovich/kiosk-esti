import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.client_screen import ClientScreen
from screens.produit_screen import ProduitScreen
from screens.vente_screen import VenteScreen
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.home_screen import HomeScreen
from kivymd.app import MDApp


class EpicerieApp(MDApp):
    icon = "assets/logo.png" 
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.utilisateur_role = None
        self.utilisateur_id = None  # Stocke l'id de l'utilisateur connecté
        self.sm = None
    
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(RegisterScreen(name="register"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.ajouter_ecrans_utilisateur()
        self.ajouter_vente_screen_utilisateur()

        self.sm.current = "login"
        return self.sm

    def ajouter_vente_screen_utilisateur(self):
        if self.sm.has_screen("ventes"):
            self.sm.remove_widget(self.sm.get_screen("ventes"))
        self.sm.add_widget(VenteScreen(name="ventes", utilisateur_id=self.utilisateur_id))

    def ajouter_ecrans_utilisateur(self):
        # Supprime les écrans existants si déjà présents
        if self.sm.has_screen("clients"):
            self.sm.remove_widget(self.sm.get_screen("clients"))
        if self.sm.has_screen("produits"):
            self.sm.remove_widget(self.sm.get_screen("produits"))
        # Ajoute les écrans avec le bon utilisateur_id
        self.sm.add_widget(ClientScreen(name="clients", utilisateur_id=self.utilisateur_id))
        self.sm.add_widget(ProduitScreen(name="produits", utilisateur_id=self.utilisateur_id))

if __name__ == "__main__":
    EpicerieApp().run()
