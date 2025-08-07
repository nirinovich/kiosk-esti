from database.database import get_connexion

def ajouter_detail_vente(vente_id, produit_id, quantite, prix_total):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        INSERT INTO details_ventes (vente_id, produit_id, quantite, prix_total)
        VALUES (?, ?, ?, ?)
    """, (vente_id, produit_id, quantite, prix_total))
    conn.commit()
    conn.close()

def get_details_par_vente(vente_id):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        SELECT * FROM details_ventes WHERE vente_id = ?
    """, (vente_id,))
    details = curseur.fetchall()
    conn.close()
    return details

def supprimer_details_par_vente(vente_id):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        DELETE FROM details_ventes WHERE vente_id = ?
    """, (vente_id,))
    conn.commit()
    conn.close()
