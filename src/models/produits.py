from database.database import get_connexion

def ajouter_produit(nom, categorie, prix_unitaire, stock, utilisateur_id):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        INSERT INTO produits (nom, categorie, prix_unitaire, stock, utilisateur_id)
        VALUES (?, ?, ?, ?, ?)
    """,(nom, categorie, prix_unitaire, stock, utilisateur_id))
    conn.commit()
    conn.close()

def mettre_a_jour_stock(produit_id, nouvelle_quantite):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        UPDATE produits SET stock = ? WHERE id = ?
    """,(nouvelle_quantite, produit_id))
    conn.commit()
    conn.close()

def get_produit(produit_id):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        SELECT * FROM produits WHERE id = ?
    """,(produit_id,))
    produit = curseur.fetchone()
    conn.close()
    return produit

def supprimer_produit(id):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM produits WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def lister_produits(utilisateur_id):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("SELECT * FROM produits WHERE utilisateur_id = ?", (utilisateur_id,))
    produits = cur.fetchall()
    conn.close()
    return produits



