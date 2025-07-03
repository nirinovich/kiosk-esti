from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
from kivy.app import App
from controllers.vente_controller import VenteController

Builder.load_file("kv/statistique_screen.kv")

class StatistiqueScreen(Screen):
    argent_encaisse = StringProperty("0 Ar")
    produits_vendus = ListProperty([])
    periode = StringProperty('jour')  # Pour le filtre actif

    def on_pre_enter(self):
        app = App.get_running_app()
        utilisateur_id = app.utilisateur_id
        self.afficher_stats_utilisateur(utilisateur_id)
        self.afficher_produits_vendus(self.periode)

    def afficher_stats_utilisateur(self, utilisateur_id):
        # Récupère toutes les ventes de l'utilisateur
        ventes = [v for v in VenteController().charger_ventes() if v[3] == utilisateur_id]
        argent_encaisse = sum(v[4] for v in ventes)
        self.argent_encaisse = f"{argent_encaisse:,.0f} Ar" if argent_encaisse else "0 Ar"

    def set_periode(self, periode):
        self.periode = periode
        self.afficher_produits_vendus(periode)

    def afficher_produits_vendus(self, periode):
        # À remplacer par la vraie récupération des produits vendus selon la période
        exemples = {
            'jour': [("Riz 5kg", 12), ("Huile", 8), ("Sucre", 5)],
            '7j': [("Riz 5kg", 50), ("Huile", 30), ("Sucre", 20), ("Pâtes", 10)],
            'mois': [("Riz 5kg", 200), ("Huile", 120), ("Sucre", 80), ("Pâtes", 40), ("Lait", 25)],
            'annee': [("Riz 5kg", 1200), ("Huile", 900), ("Sucre", 700), ("Pâtes", 400), ("Lait", 250), ("Café", 100)]
        }
        produits = exemples.get(periode, [])
        self.ids.produits_vendus_list.clear_widgets()
        for i, (prod, quantite) in enumerate(produits, 1):
            from kivymd.uix.boxlayout import MDBoxLayout
            from kivymd.uix.label import MDLabel
            from kivymd.uix.button import MDIconButton
            from kivymd.uix.badge import MDBadge
            line = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=12, padding=[8,0,8,0])
            line.add_widget(MDLabel(text=f"{i}. {prod}", font_size="16sp", theme_text_color="Primary", halign="left"))
            line.add_widget(MDBadge(text=str(quantite), md_bg_color=(0.1, 0.5, 0.9, 1) if i==1 else (0.7, 0.7, 0.7, 1)))
            if i == 1:
                line.add_widget(MDIconButton(icon="star", theme_icon_color="Custom", icon_color=(1, 0.8, 0, 1), font_size="20sp"))
            self.ids.produits_vendus_list.add_widget(line)