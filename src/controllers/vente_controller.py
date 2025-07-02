from models.vente import ajouter_vente, get_vente, lister_ventes, supprimer_vente
from models.detail_vente import ajouter_detail_vente
from controllers.produit_controller import ProduitController
from datetime import datetime

class VenteController:
    def __init__(self):
        self.ventes = []

    def charger_ventes(self):
        self.ventes = lister_ventes()
        return self.ventes

    def creer_vente(self, client_id, utilisateur_id, panier):
        """
        panier = liste de produits achetés :
        [{'produit_id': int, 'quantite': int, 'prix_total': float}, ...]
        """
        date_vente = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = sum(item['prix_total'] for item in panier)

        vente_id = ajouter_vente(date_vente, client_id, utilisateur_id, total)

        produit_controller = ProduitController(utilisateur_id=utilisateur_id)
        for item in panier:
            ajouter_detail_vente(vente_id, item['produit_id'], item['quantite'], item['prix_total'])
            # Diminuer le stock du produit vendu
            produit = produit_controller.get_produit(item['produit_id'])
            if produit:
                nouveau_stock = produit[4] - item['quantite']  # produit[4] = stock
                if nouveau_stock < 0:
                    nouveau_stock = 0
                produit_controller.modifier_stock(item['produit_id'], nouveau_stock)

        return vente_id

    def supprimer_vente(self, vente_id):
        supprimer_vente(vente_id)

    def get_vente(self, vente_id):
        return get_vente(vente_id)
