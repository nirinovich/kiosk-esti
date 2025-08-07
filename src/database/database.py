import sqlite3

# Connexion à la base de données
def get_connexion():
    return sqlite3.connect('epicerie.db')

connexion = get_connexion()
curseur = connexion.cursor()

# Table : utilisateurs
curseur.execute("""CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'vendeur')) NOT NULL)
""")

# Table : produits
curseur.execute("""CREATE TABLE IF NOT EXISTS produits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    categorie TEXT,
    prix_unitaire REAL NOT NULL,
    stock INTEGER NOT NULL,
    utilisateur_id INTEGER,
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id))
""")

# Table : clients
curseur.execute("""CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    telephone TEXT,
    adresse TEXT,
    utilisateur_id INTEGER,
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id))
""")

# Table : ventes
curseur.execute("""CREATE TABLE IF NOT EXISTS ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_vente TEXT NOT NULL,
    client_id INTEGER,
    utilisateur_id INTEGER,
    total REAL,
    FOREIGN KEY(client_id) REFERENCES clients(id),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id))
""")

# Table : details_ventes
curseur.execute("""CREATE TABLE IF NOT EXISTS details_ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vente_id INTEGER,
    produit_id INTEGER,
    quantite INTEGER,
    prix_total REAL,
    FOREIGN KEY(vente_id) REFERENCES ventes(id),
    FOREIGN KEY(produit_id) REFERENCES produits(id))
""")

# Enregistrement des modifications et fermeture de la connexion
connexion.commit()
connexion.close()

