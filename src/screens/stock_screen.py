from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from functools import partial

Builder.load_file("kv/stock_screen.kv")

class StockScreen(Screen):
    produits = ListProperty([])

    def on_pre_enter(self):
        self.charger_produits()

    def charger_produits(self):
        # Récupère la liste des produits (tuples) depuis le contrôleur du screen 'produits'
        produits_tuples = self.manager.get_screen('produits').controller.charger_produits()
        # Conversion tuple -> dict pour l'affichage dans StockScreen
        produits = []
        for p in produits_tuples:
            # p = (id, nom, categorie, prix_unitaire, stock, utilisateur_id)
            produits.append({
                'id': p[0],
                'nom': p[1],
                'categorie': p[2],
                'prix_unitaire': p[3],
                'stock': p[4],
                'utilisateur_id': p[5],
                'seuil': 5,  # seuil d'alerte par défaut, à adapter si besoin
                'unite': 'pièce'  # unité par défaut
            })
        self.produits = produits
        self.afficher_produits(self.produits)

    def afficher_produits(self, produits):
        self.ids.stock_list.clear_widgets()
        # En-tête interactif et coloré
        def header_btn(text, champ):
            btn = Button(
                text=text,
                size_hint_x={
                    "ID": 0.08, "Nom": 0.22, "Catégorie": 0.18, "Prix": 0.15, "Stock": 0.13, "Devise": 0.11
                }[text],
                background_color=(0.2, 0.4, 0.8, 1),
                color=(1, 1, 1, 1),
                bold=True,
                font_size=16
            )
            if champ:
                btn.bind(on_release=lambda x: self.trier_par(champ))
            return btn
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=44, spacing=5)
        # header.add_widget(header_btn("ID", "id"))  # Suppression de la colonne ID
        header.add_widget(header_btn("Nom", "nom"))
        header.add_widget(header_btn("Catégorie", "categorie"))
        header.add_widget(header_btn("Prix", "prix_unitaire"))
        header.add_widget(header_btn("Stock", "stock"))
        header.add_widget(header_btn("Devise", None))
        # Colonne actions à droite (même style que les autres)
        header.add_widget(Button(
            text="Actions",
            size_hint_x=0.22,
            background_color=(0.2, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=16
        ))
        self.ids.stock_list.add_widget(header)

        for i, prod in enumerate(produits):
            # Alternance de couleurs de lignes
            if prod['stock'] <= prod.get('seuil', 5):
                bg_color = (1, 0.85, 0.85, 1)  # rouge très clair
                fg_color = (0.7, 0.1, 0.1, 1)
            elif i % 2 == 0:
                bg_color = (0.95, 0.97, 1, 1)  # bleu très pâle
                fg_color = (0.15, 0.15, 0.15, 1)
            else:
                bg_color = (1, 1, 1, 1)
                fg_color = (0.15, 0.15, 0.15, 1)
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=38, spacing=5)
            # Fond coloré
            with box.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(*bg_color)
                Rectangle(pos=box.pos, size=box.size)
            # box.add_widget(Label(text=str(prod['id']), size_hint_x=0.08, color=fg_color, bold=True, font_size=15))  # Suppression de l'affichage ID
            box.add_widget(Label(text=prod['nom'], size_hint_x=0.22, color=fg_color, font_size=15))
            box.add_widget(Label(text=prod['categorie'], size_hint_x=0.18, color=fg_color, font_size=15))
            box.add_widget(Label(text=f"{prod['prix_unitaire']}", size_hint_x=0.15, color=fg_color, font_size=15))
            # Badge stock bas
            if prod['stock'] <= prod.get('seuil', 5):
                stock_label = Label(
                    text=f"[b]{prod['stock']}[/b]", markup=True,
                    size_hint_x=0.13, color=(0.8, 0.1, 0.1, 1), font_size=15
                )
            else:
                stock_label = Label(text=str(prod['stock']), size_hint_x=0.13, color=fg_color, font_size=15)
            box.add_widget(stock_label)
            box.add_widget(Label(text="Ar", size_hint_x=0.11, color=fg_color, font_size=15))
            # Colonne action compacte à droite
            btn_add = Button(
                text="Ajouter",
                size_hint_x=0.5,
                height=32,
                background_color=(0.2, 0.7, 0.2, 1),
                color=(1, 1, 1, 1),
                font_size=13,
                bold=True,
                padding=[0, 0],
                halign="center",
                valign="middle"
            )
            btn_add.bind(on_release=partial(self.ouvrir_popup_ajout_quantite, prod))
            btn_retirer = Button(
                text="Retirer",
                size_hint_x=0.5,
                height=32,
                background_color=(0.95, 0.6, 0.1, 1),
                color=(1, 1, 1, 1),
                font_size=13,
                bold=True,
                padding=[0, 0],
                halign="center",
                valign="middle"
            )
            btn_retirer.bind(on_release=partial(self.ouvrir_popup_retrait_quantite, prod))
            action_box = BoxLayout(orientation='horizontal', size_hint_x=0.22, spacing=0, padding=[0,0,0,0])
            action_box.add_widget(btn_add)
            action_box.add_widget(btn_retirer)
            box.add_widget(action_box)
            self.ids.stock_list.add_widget(box)

    def modifier_stock(self, produit, delta):
        produit['stock'] += delta
        if produit['stock'] < 0:
            produit['stock'] = 0
        # Ici, tu dois mettre à jour la BDD ou le contrôleur
        self.charger_produits()

    def ouvrir_popup_ajout(self):
        self._ouvrir_popup_produit("Ajouter un produit")

    def ouvrir_popup_modif(self, produit):
        self._ouvrir_popup_produit("Modifier le produit", produit)

    def _ouvrir_popup_produit(self, titre, produit=None):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        nom_input = TextInput(hint_text="Nom", multiline=False, size_hint_y=None, height=40, font_size=16)
        stock_input = TextInput(hint_text="Stock", multiline=False, size_hint_y=None, height=40, font_size=16, input_filter='int')
        if produit:
            nom_input.text = produit['nom']
            stock_input.text = str(produit['stock'])
        box.add_widget(nom_input)
        box.add_widget(stock_input)
        btns = BoxLayout(spacing=10, size_hint_y=None, height=40)
        def save(instance):
            nom = nom_input.text
            stock = int(stock_input.text) if stock_input.text.isdigit() else 0
            if not nom:
                return
            if produit:
                produit['nom'] = nom
                produit['stock'] = stock
                # update in BDD
            else:
                # ajouter dans la BDD
                self.produits.append({'nom': nom, 'stock': stock})
            self.charger_produits()
            popup.dismiss()
        btn_save = Button(text="Enregistrer", on_release=save)
        btn_cancel = Button(text="Annuler", on_release=lambda x: popup.dismiss())
        btns.add_widget(btn_save)
        btns.add_widget(btn_cancel)
        box.add_widget(btns)
        popup = Popup(title=titre, content=box, size_hint=(0.7,0.5))
        popup.open()

    def supprimer_produit(self, produit, *args):
        self.manager.get_screen('produits').controller.supprimer_produit(produit['id'])
        self.charger_produits()

    def filtrer(self, texte):
        texte = texte.lower()
        filtres = [p for p in self.produits if texte in p['nom'].lower() or texte in str(p['stock'])]
        self.afficher_produits(filtres)

    def trier_par(self, champ, reverse=False):
        if champ not in ['id', 'nom', 'categorie', 'prix_unitaire', 'stock']:
            return
        self.produits = sorted(self.produits, key=lambda p: p[champ], reverse=reverse)
        self.afficher_produits(self.produits)

    def ouvrir_popup_ajout_quantite(self, produit, *args):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        info = Label(text=f"Ajouter à {produit['nom']} (stock actuel: {produit['stock']})", size_hint_y=None, height=40)
        qte_input = TextInput(hint_text="Quantité à ajouter", multiline=False, size_hint_y=None, height=40, font_size=16, input_filter='int')
        box.add_widget(info)
        box.add_widget(qte_input)
        btns = BoxLayout(spacing=10, size_hint_y=None, height=40)
        def ajouter(instance):
            qte = int(qte_input.text) if qte_input.text.isdigit() else 0
            if qte > 0:
                nouveau_stock = produit['stock'] + qte
                self.manager.get_screen('produits').controller.modifier_stock(produit['id'], nouveau_stock)
                self.charger_produits()
            popup.dismiss()
        btn_add = Button(text="Ajouter", on_release=ajouter)
        btn_cancel = Button(text="Annuler", on_release=lambda x: popup.dismiss())
        btns.add_widget(btn_add)
        btns.add_widget(btn_cancel)
        box.add_widget(btns)
        popup = Popup(title="Ajouter quantité", content=box, size_hint=(0.6,0.4))
        popup.open()

    def ouvrir_popup_retrait_quantite(self, produit, *args):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        info = Label(text=f"Retirer de {produit['nom']} (stock actuel: {produit['stock']})", size_hint_y=None, height=40)
        qte_input = TextInput(hint_text="Quantité à retirer", multiline=False, size_hint_y=None, height=40, font_size=16, input_filter='int')
        box.add_widget(info)
        box.add_widget(qte_input)
        btns = BoxLayout(spacing=10, size_hint_y=None, height=40)
        def retirer(instance):
            qte = int(qte_input.text) if qte_input.text.isdigit() else 0
            if qte > 0 and qte <= produit['stock']:
                nouveau_stock = produit['stock'] - qte
                self.manager.get_screen('produits').controller.modifier_stock(produit['id'], nouveau_stock)
                self.charger_produits()
            popup.dismiss()
        btn_retirer = Button(text="Retirer", on_release=retirer)
        btn_cancel = Button(text="Annuler", on_release=lambda x: popup.dismiss())
        btns.add_widget(btn_retirer)
        btns.add_widget(btn_cancel)
        box.add_widget(btns)
        popup = Popup(title="Retirer quantité", content=box, size_hint=(0.6,0.4))
        popup.open()