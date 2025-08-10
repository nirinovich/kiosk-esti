import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import io

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

from kivy.app import App
from controllers.vente_controller import VenteController
from models.detail_vente import get_details_par_vente
from models.produits import get_produit
from datetime import datetime, timedelta

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
        self.afficher_graphique(self.periode)

    def afficher_stats_utilisateur(self, utilisateur_id):
        ventes = [v for v in VenteController().charger_ventes() if v[3] == utilisateur_id]
        argent_encaisse = sum(v[4] for v in ventes)
        self.argent_encaisse = f"{argent_encaisse:,.0f} Ar" if argent_encaisse else "0 Ar"

    def set_periode(self, periode):
        self.periode = periode
        self.afficher_produits_vendus(periode)
        self.afficher_graphique(periode)

    def _filtrer_ventes_par_periode(self, ventes, periode):
        now = datetime.now()
        if periode == 'jour':
            return [v for v in ventes if datetime.strptime(v[1], "%Y-%m-%d %H:%M:%S").date() == now.date()]
        elif periode == '7j':
            il_y_a_7j = now - timedelta(days=7)
            return [v for v in ventes if datetime.strptime(v[1], "%Y-%m-%d %H:%M:%S") >= il_y_a_7j]
        elif periode == 'mois':
            return [v for v in ventes if datetime.strptime(v[1], "%Y-%m-%d %H:%M:%S").month == now.month and datetime.strptime(v[1], "%Y-%m-%d %H:%M:%S").year == now.year]
        elif periode == 'annee':
            return [v for v in ventes if datetime.strptime(v[1], "%Y-%m-%d %H:%M:%S").year == now.year]
        else:
            return ventes

    def _get_top_produits(self, ventes):
        # ventes: liste de tuples (id, date_vente, client_id, utilisateur_id, total)
        produits_count = {}
        for v in ventes:
            details = get_details_par_vente(v[0])
            for d in details:
                produit_id = d[2]
                quantite = d[3]
                if produit_id not in produits_count:
                    produits_count[produit_id] = 0
                produits_count[produit_id] += quantite
        # Récupérer les noms de produits
        produits = []
        for pid, qte in produits_count.items():
            prod = get_produit(pid)
            if prod:
                produits.append((prod[1], qte))  # prod[1]=nom
        produits.sort(key=lambda x: x[1], reverse=True)
        return produits

    def afficher_produits_vendus(self, periode):
        ventes = VenteController().charger_ventes()
        ventes = self._filtrer_ventes_par_periode(ventes, periode)
        # On veut afficher tous les produits vendus (même ceux vendus une seule fois)
        top_produits = self._get_top_produits(ventes)
        self.ids.produits_vendus_list.clear_widgets()
        for i, (prod, quantite) in enumerate(top_produits, 1):
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
        # Si aucun produit vendu, afficher un message
        if not top_produits:
            from kivymd.uix.label import MDLabel
            self.ids.produits_vendus_list.add_widget(
                MDLabel(text="Aucun produit vendu pour cette période.", halign="center", theme_text_color="Hint", font_size="16sp")
            )

    def afficher_graphique(self, periode):
        ventes = VenteController().charger_ventes()
        ventes = self._filtrer_ventes_par_periode(ventes, periode)
        top_produits = self._get_top_produits(ventes)
        noms = [p[0] for p in top_produits]
        quantites = [p[1] for p in top_produits]
        plt.figure(figsize=(9, 4))  # Agrandit la taille du graphique
        bars = plt.bar(noms, quantites, color=['#1976D2' if i==0 else '#90CAF9' for i in range(len(noms))], edgecolor='#1565C0', linewidth=2)
        plt.title('Produits les plus vendus', fontsize=18, color='#1976D2', weight='bold')
        plt.xlabel('Produit', fontsize=14)
        plt.ylabel('Quantité', fontsize=14)
        plt.xticks(rotation=20, ha='right', fontsize=12)
        plt.yticks(fontsize=12)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.7, int(yval), ha='center', va='bottom', fontsize=12, color='#1976D2', weight='bold')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=140, bbox_inches='tight', transparent=True)
        plt.close()
        buf.seek(0)
        from kivy.core.image import Image as CoreImage
        core_image = CoreImage(buf, ext='png')
        self.ids.graph_image.texture = core_image.texture
        buf.close()