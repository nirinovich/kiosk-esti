from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers.vente_controller import VenteController
from controllers.client_controller import ClientController
from controllers.produit_controller import ProduitController
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("kv/vente_screen.kv")

class VenteScreen(Screen):
    clients = ListProperty([])
    produits = ListProperty([])
    panier = ListProperty([])
    message = StringProperty("")
    total = NumericProperty(0)

    def __init__(self, utilisateur_id=None, **kwargs):
        super().__init__(**kwargs)
        self.vente_ctrl = VenteController()
        self.client_ctrl = ClientController(utilisateur_id=utilisateur_id)
        self.produit_ctrl = ProduitController(utilisateur_id=utilisateur_id)
        self.charger_clients()
        self.charger_produits()
        self.panier = []

    def charger_clients(self):
        self.clients = self.client_ctrl.charger_clients()

    def charger_produits(self):
        self.produits = self.produit_ctrl.charger_produits()

    def filtrer_produits(self, texte):
        tous = self.produit_ctrl.charger_produits()
        texte = texte.lower()
        self.produits = [p for p in tous if texte in p[1].lower() or texte in (p[2] or '').lower()]
        # Mettre à jour le spinner
        self.ids.produit_spinner.values = [str(p[1]) for p in self.produits]

    def afficher_panier(self):
        self.ids.panier_list.clear_widgets()
        for item in self.panier:
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, padding=[5,0,5,0], spacing=5)
            box.add_widget(Label(text=f"{item['nom']}", size_hint_x=0.4, color=(0.1,0.1,0.1,1), bold=True))
            box.add_widget(Label(text=f"x{item['quantite']}", size_hint_x=0.2, color=(0.2,0.2,0.2,1)))
            box.add_widget(Label(text=f"{item['prix_total']} Ar", size_hint_x=0.25, color=(0.2,0.2,0.2,1)))
            btn_suppr = Button(text="Supprimer", size_hint_x=0.15, background_color=(0.8,0.1,0.1,1), color=(1,1,1,1), font_size=14)
            btn_suppr.bind(on_release=lambda btn, pid=item['produit_id']: self.supprimer_du_panier(pid))
            box.add_widget(btn_suppr)
            self.ids.panier_list.add_widget(box)

    def ajouter_au_panier(self, produit_id, quantite):
        try:
            quant = int(quantite)
            if quant <= 0:
                self.message = "Quantité doit être > 0"
                return
        except:
            self.message = "Quantité invalide"
            return

        produit = self.produit_ctrl.get_produit(produit_id)
        if not produit:
            self.message = "Produit introuvable"
            return

        prix_total = produit[3] * quant  # prix_unitaire * quant

        # Vérifier si déjà dans panier
        for item in self.panier:
            if item['produit_id'] == produit_id:
                item['quantite'] += quant
                item['prix_total'] += prix_total
                self.calculer_total()
                self.message = "Produit ajouté au panier"
                self.afficher_panier()
                return

        self.panier.append({
            'produit_id': produit_id,
            'nom': produit[1],
            'quantite': quant,
            'prix_total': prix_total
        })
        self.calculer_total()
        self.message = "Produit ajouté au panier"
        self.afficher_panier()

    def supprimer_du_panier(self, produit_id):
        self.panier = [item for item in self.panier if item['produit_id'] != produit_id]
        self.calculer_total()
        self.afficher_panier()

    def calculer_total(self):
        self.total = sum(item['prix_total'] for item in self.panier)

    def valider_vente(self, client_id, utilisateur_id=1):
        # utilisateur_id statique pour test, à adapter
        if not self.panier:
            self.message = "Le panier est vide"
            return

        if not client_id:
            self.message = "Sélectionnez un client"
            return

        vente_id = self.vente_ctrl.creer_vente(client_id, utilisateur_id, self.panier)
        self.panier = []
        self.calculer_total()
        self.afficher_panier()
        self.message = f"Vente enregistrée (ID: {vente_id})"
        self.charger_produits()  # pour rafraîchir stock si tu as gestion stock dans controller
        # Afficher une popup de confirmation
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text=f"Vente enregistrée avec succès !\nID : {vente_id}", font_size=18))
        btn_ok = Button(text="OK", size_hint_y=None, height=40)
        box.add_widget(btn_ok)
        popup = Popup(title="Confirmation", content=box, size_hint=(0.5,0.3))
        btn_ok.bind(on_release=popup.dismiss)
        popup.open()
        # Réinitialiser les sélections
        self.ids.client_spinner.text = "Sélectionner un client"
        self.ids.produit_spinner.text = "Sélectionner un produit"

    def on_pre_enter(self):
        self.charger_clients()
        self.charger_produits()
        self.ids.produit_spinner.values = [str(p[1]) for p in self.produits]
        self.ids.client_spinner.values = [str(c[1]) for c in self.clients]
        self.afficher_panier()
