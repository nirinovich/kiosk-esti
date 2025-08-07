import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers.client_controller import ClientController
from kivy.properties import ListProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button as KivyButton

Builder.load_file("kv/client_screen.kv")

class ClientScreen(Screen):
    clients = ListProperty([])
    message = StringProperty("")

    def __init__(self, utilisateur_id=None, **kwargs):
        self.utilisateur_id = utilisateur_id
        super().__init__(**kwargs)
        self.controller = ClientController(utilisateur_id=self.utilisateur_id)
        self.charger_clients()

    def charger_clients(self):
        self.clients = self.controller.charger_clients()
        self.filtrer_clients("")

    def filtrer_clients(self, texte):
        tous = self.controller.charger_clients()
        texte = texte.lower()
        self.clients = [c for c in tous if texte in c[1].lower() or texte in (c[2] or '').lower() or texte in (c[3] or '').lower()]
        self.ids.client_list.clear_widgets()
        for client in self.clients:
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            box.add_widget(Label(text=f"{client[1]} - {client[2]} - {client[3]}", size_hint_x=0.8, color=(0.1,0.1,0.1,1)))
            btn_suppr = Button(text="Supprimer", size_hint_x=0.2, background_color=(0.8,0.1,0.1,1), color=(1,1,1,1))
            btn_suppr.bind(on_release=lambda btn, c_id=client[0]: self.supprimer_client(c_id))
            box.add_widget(btn_suppr)
            self.ids.client_list.add_widget(box)

    def ajouter_client(self, nom, telephone, adresse):
        try:
            if not nom:
                self.message = "Le nom du client est obligatoire."
                return
            self.controller.ajouter_client(nom, telephone, adresse)
            self.message = "Client ajouté avec succès."
            self.ids.nom_input.text = ""
            self.ids.tel_input.text = ""
            self.ids.adresse_input.text = ""
            self.charger_clients()
        except Exception as e:
            self.message = f"Erreur : {str(e)}"

    def supprimer_client(self, client_id):
        def do_delete(instance):
            self.controller.supprimer_client(client_id)
            self.message = "Client supprimé."
            self.charger_clients()
            popup.dismiss()
        def cancel(instance):
            popup.dismiss()
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text="Voulez-vous vraiment supprimer ce client ?"))
        btns = BoxLayout(spacing=10, size_hint_y=None, height=40)
        btn_yes = KivyButton(text="Oui", on_release=do_delete)
        btn_no = KivyButton(text="Non", on_release=cancel)
        btns.add_widget(btn_yes)
        btns.add_widget(btn_no)
        box.add_widget(btns)
        popup = Popup(title="Confirmation", content=box, size_hint=(0.6,0.3))
        popup.open()

    def ouvrir_popup_ajout(self):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        nom_input = self._popup_input('Nom')
        tel_input = self._popup_input('Téléphone')
        adresse_input = self._popup_input('Adresse')
        box.add_widget(nom_input)
        box.add_widget(tel_input)
        box.add_widget(adresse_input)
        btns = BoxLayout(spacing=10, size_hint_y=None, height=40)
        btn_add = KivyButton(text="Ajouter", on_release=lambda x: self._ajouter_client_popup(nom_input.text, tel_input.text, adresse_input.text, popup))
        btn_cancel = KivyButton(text="Annuler", on_release=lambda x: popup.dismiss())
        btns.add_widget(btn_add)
        btns.add_widget(btn_cancel)
        box.add_widget(btns)
        popup = Popup(title="Ajouter un client", content=box, size_hint=(0.7,0.5))
        popup.open()

    def _popup_input(self, hint):
        from kivy.uix.textinput import TextInput
        return TextInput(hint_text=hint, multiline=False, size_hint_y=None, height=40, font_size=16)

    def _ajouter_client_popup(self, nom, tel, adresse, popup):
        if not nom:
            self.message = "Le nom du client est obligatoire."
            return
        self.controller.ajouter_client(nom, tel, adresse)
        self.message = "Client ajouté avec succès."
        self.charger_clients()
        popup.dismiss()
