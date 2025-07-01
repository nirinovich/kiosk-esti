from models.produits import ajouter_produit, mettre_a_jour_stock, get_produit, supprimer_produit, lister_produits

class ProduitController:
    def __init__(self, utilisateur_id=None):
        self.produits = []
        self.utilisateur_id = utilisateur_id

    def charger_produits(self):
        self.produits = lister_produits(self.utilisateur_id)
        return self.produits

    def ajouter_produit(self, nom, categorie, prix_unitaire, stock):
        if not nom:
            raise ValueError("Le nom du produit est obligatoire.")
        ajouter_produit(nom, categorie, prix_unitaire, stock, self.utilisateur_id)

    def modifier_stock(self, produit_id, nouvelle_quantite):
        mettre_a_jour_stock(produit_id, nouvelle_quantite)

    def supprimer_produit(self, produit_id):
        supprimer_produit(produit_id)

    def get_produit(self, produit_id):
        return get_produit(produit_id)
