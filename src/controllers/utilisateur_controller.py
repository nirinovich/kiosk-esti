from models.utilisateurs import ajouter_utilisateur, verifier_utlisateur, obtenir_role, supprimer_utilisateur, lister_utilisateurs
from models.utilisateurs import verifier_utlisateur
class UtilisateurController:
    def inscrire_utilisateur(self, nom, email, mot_de_passe, role):
        if not nom or not email or not mot_de_passe:
            raise ValueError("Tous les champs sont obligatoires.")
        ajouter_utilisateur(nom, email, mot_de_passe, role)

    def connexion_utilisateur(self, email, mot_de_passe):
        return verifier_utlisateur(email, mot_de_passe)

    def get_role(self, email):
        return obtenir_role(email)

    def supprimer_utilisateur(self, utilisateur_id):
        supprimer_utilisateur(utilisateur_id)

    def lister_utilisateurs(self):
        return lister_utilisateurs()
    

def verifier_connexion(email, mot_de_passe):
    return verifier_utlisateur(email, mot_de_passe)