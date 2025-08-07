from models.detail_vente import ajouter_detail_vente, get_details_par_vente, supprimer_details_par_vente

class DetailVenteController:
    def ajouter_detail(self, vente_id, produit_id, quantite, prix_total):
        ajouter_detail_vente(vente_id, produit_id, quantite, prix_total)

    def charger_details(self, vente_id):
        return get_details_par_vente(vente_id)

    def supprimer_details(self, vente_id):
        supprimer_details_par_vente(vente_id)
