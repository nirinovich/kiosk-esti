import random
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers.produit_controller import ProduitController
from kivy.properties import ListProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button as KivyButton

Builder.load_file("kv/produit_screen.kv")

class ProduitScreen(Screen):
    produits = ListProperty([])
    message = StringProperty("")

    def __init__(self, utilisateur_id=None, **kwargs):
        super().__init__(**kwargs)
        self.utilisateur_id = utilisateur_id
        self.controller = ProduitController(utilisateur_id=self.utilisateur_id)
        self.charger_produits()

    def ouvrir_popup_ajout(self):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        nom_input = self._popup_input('Nom')
        cat_input = self._popup_input('Catégorie')
        prix_input = self._popup_input('Prix unitaire', input_filter='float')
        stock_input = self._popup_input('Stock', input_filter='int')
        box.add_widget(nom_input)
        box.add_widget(cat_input)
        box.add_widget(prix_input)
        box.add_widget(stock_input)
        btns = BoxLayout(spacing=10, size_hint_y=None, height=40)
        btn_add = KivyButton(text="Ajouter", on_release=lambda x: self._ajouter_produit_popup(nom_input.text, cat_input.text, prix_input.text, stock_input.text, popup))
        btn_cancel = KivyButton(text="Annuler", on_release=lambda x: popup.dismiss())
        btns.add_widget(btn_add)
        btns.add_widget(btn_cancel)
        box.add_widget(btns)
        popup = Popup(title="Ajouter un produit", content=box, size_hint=(0.7,0.7))
        popup.open()

    def _popup_input(self, hint, input_filter=None):
        from kivy.uix.textinput import TextInput
        return TextInput(hint_text=hint, multiline=False, size_hint_y=None, height=40, font_size=16, input_filter=input_filter)

    def _ajouter_produit_popup(self, nom, cat, prix, stock, popup):
        try:
            prix_val = float(prix)
            stock_val = int(stock)
            if not nom:
                self.message = "Le nom du produit est obligatoire."
                return
            self.controller.ajouter_produit(nom, cat, prix_val, stock_val)
            self.message = "Produit ajouté avec succès."
            self.charger_produits()
            popup.dismiss()
        except ValueError:
            self.message = "Prix et stock doivent être des nombres valides."

    def filtrer_produits(self, texte):
        tous = self.controller.charger_produits()
        texte = texte.lower()
        self.produits = [p for p in tous if texte in p[1].lower() or texte in (p[2] or '').lower()]
        self.afficher_produits()

    def afficher_produits(self):
        self.ids.produit_list.clear_widgets()
        for produit in self.produits:
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            box.add_widget(Label(text=f"{produit[1]} | Cat: {produit[2]} | Prix: {produit[3]} | Stock: {produit[4]}", size_hint_x=0.7, color=(0.1,0.1,0.1,1)))
            btn_suppr = Button(text="Supprimer", size_hint_x=0.15, background_color=(0.8,0.1,0.1,1), color=(1,1,1,1))
            btn_suppr.bind(on_release=lambda btn, pid=produit[0]: self.supprimer_produit(pid))
            box.add_widget(btn_suppr)
            self.ids.produit_list.add_widget(box)

    def charger_produits(self):
        self.produits = self.controller.charger_produits()
        self.afficher_produits()

    def ajouter_produit(self, nom, categorie, prix, stock):
        try:
            prix_val = float(prix)
            stock_val = int(stock)
            if not nom:
                self.message = "Le nom du produit est obligatoire."
                return
            self.controller.ajouter_produit(nom, categorie, prix_val, stock_val)
            self.message = "Produit ajouté avec succès."
            self.ids.nom_input.text = ""
            self.ids.categorie_input.text = ""
            self.ids.prix_input.text = ""
            self.ids.stock_input.text = ""
            self.charger_produits()
        except ValueError:
            self.message = "Prix et stock doivent être des nombres valides."

    def supprimer_produit(self, produit_id):
        def do_delete(instance):
            self.controller.supprimer_produit(produit_id)
            self.message = "Produit supprimé."
            self.charger_produits()
            popup.dismiss()
        def cancel(instance):
            popup.dismiss()
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text="Voulez-vous vraiment supprimer ce produit ?"))
        btns = BoxLayout(spacing=10, size_hint_y=None, height=40)
        btn_yes = KivyButton(text="Oui", on_release=do_delete)
        btn_no = KivyButton(text="Non", on_release=cancel)
        btns.add_widget(btn_yes)
        btns.add_widget(btn_no)
        box.add_widget(btns)
        popup = Popup(title="Confirmation", content=box, size_hint=(0.6,0.3))
        popup.open()

    def importer_produits_exemple(self):
        exemples = [
            ("Riz local 5kg", "Aliment sec", 8000),
            ("Spaghetti 500g", "Aliment sec", 3000),
            ("Farine de blé 1kg", "Aliment sec", 2500),
            ("Bonbons mix", "Confiserie", 500),
            ("Biscuit sachet", "Snack", 1500),
            ("Chocolat tablette", "Snack", 2500),
            ("Savon 100g", "Hygiène", 1000),
            ("Dentifrice 75ml", "Hygiène", 1500),
            ("Papier toilette (4 rouleaux)", "Hygiène", 2500),
            ("Liquide vaisselle 1L", "Ménager", 3000),
            ("Poudre à laver 500g", "Ménager", 2500),
            ("Allumettes boîte", "Ménager", 200),
            ("Huile 1L", "Condiment", 6500),
            ("Sel fin 1kg", "Condiment", 1000),
            ("Sucre 1kg", "Condiment", 2500),
        ]
        for nom, cat, prix in exemples:
            stock = random.randint(10, 100)
            self.controller.ajouter_produit(nom, cat, prix, stock)

        self.message = "Produits d'exemple ajoutés avec succès."
        self.charger_produits()
