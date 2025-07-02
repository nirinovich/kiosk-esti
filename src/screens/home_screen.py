from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("kv/home_screen.kv")

class HomeScreen(Screen):
    pass

    def go_to_ventes(self):
        self.manager.current = "ventes"

    def go_to_produits(self):
        self.manager.current = "produits"

    def go_to_clients(self):
        self.manager.current = "clients"

    def go_to_parametres(self):
        self.manager.current = "parametres"

    def deconnexion(self):
        self.manager.current = "login"
