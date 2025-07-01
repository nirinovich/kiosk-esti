from database.database import get_connexion

def ajouter_vente(date_vente, client_id, utilisateur_id, total):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        INSERT INTO ventes (date_vente, client_id, utilisateur_id, total)
        VALUES (?, ?, ?, ?)
    """, (date_vente, client_id, utilisateur_id, total))
    conn.commit()
    vente_id = curseur.lastrowid  # Récupère l'ID de la vente ajoutée
    conn.close()
    return vente_id

def get_vente(vente_id):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        SELECT * FROM ventes WHERE id = ?
    """, (vente_id,))
    vente = curseur.fetchone()
    conn.close()
    return vente

def lister_ventes():
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM ventes")
    ventes = curseur.fetchall()
    conn.close()
    return ventes

def supprimer_vente(vente_id):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("DELETE FROM ventes WHERE id = ?", (vente_id,))
    conn.commit()
    conn.close()
