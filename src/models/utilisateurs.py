import bcrypt
from database.database import get_connexion

def ajouter_utilisateur(nom, email, mot_de_passe, role):
    conn = get_connexion()
    curseur = conn.cursor()
    # Hash the password before storing
    hashed = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
    curseur.execute("""
        INSERT INTO utilisateurs (nom, email, mot_de_passe, role) 
        VALUES(?, ?, ?, ?)        
    """, (nom, email, hashed, role))
    conn.commit()
    conn.close()

def verifier_utlisateur(email, mot_de_passe):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        SELECT * FROM utilisateurs WHERE email = ?
    """, (email,))
    utilisateur = curseur.fetchone()
    conn.close()
    if utilisateur:
        # utilisateur[3] is mot_de_passe (hashed)
        hashed = utilisateur[3]
        if bcrypt.checkpw(mot_de_passe.encode('utf-8'), hashed):
            return utilisateur
    return None

def obtenir_role(email):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        SELECT role FROM utilisateurs WHERE email = ? 
    """,(email,))
    resultat = curseur.fetchone()
    conn.close()
    return resultat

def supprimer_utilisateur(id):
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("""
        DELETE FROM utilisateurs WHERE id = ?
    """,(id,))
    conn.commit()
    conn.close()

def lister_utilisateurs():
    conn = get_connexion()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM utilisateurs")
    utilisateurs = curseur.fetchall()
    conn.close()
    return utilisateurs