from models.client import ajouter_client, get_client, lister_clients, supprimer_client

class ClientController:
    def __init__(self, utilisateur_id=None):
        self.clients = []
        self.utilisateur_id = utilisateur_id

    def charger_clients(self):
        self.clients = lister_clients(self.utilisateur_id)
        return self.clients

    def ajouter_client(self, nom, telephone, adresse):
        if not nom:
            raise ValueError("Le nom du client est obligatoire.")
        ajouter_client(nom, telephone, adresse, self.utilisateur_id)

    def supprimer_client(self, client_id):
        supprimer_client(client_id)

    def get_client(self, client_id):
        return get_client(client_id)
