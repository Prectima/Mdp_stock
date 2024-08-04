import sqlite3
import tkinter as tk
from tkinter import messagebox
import hashlib
from cryptography.fernet import Fernet
import base64

# Générer une clé de chiffrement
def generate_key():
    return Fernet.generate_key()

# Chiffrement avec la clé Fernet
def encrypt(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Déchiffrement avec la clé Fernet
def decrypt(token, key):
    fernet = Fernet(key)
    return fernet.decrypt(token).decode()

# Connexion à la base de données
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

# Création des tables pour le mot de passe maître et les mots de passe enregistrés
cursor.execute('''
CREATE TABLE IF NOT EXISTS master_password (
    id INTEGER PRIMARY KEY,
    password TEXT NOT NULL
)
''')

# Ajouter la colonne 'key' si elle n'existe pas
try:
    cursor.execute('ALTER TABLE master_password ADD COLUMN key BLOB')
except sqlite3.OperationalError:
    pass

cursor.execute('''
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY,
    site TEXT NOT NULL,
    pseudo TEXT NOT NULL,
    mdp TEXT NOT NULL
)
''')

# Fonction pour hacher les mots de passe
def hacher_mot_de_passe(mdp):
    return hashlib.sha256(mdp.encode()).hexdigest()

# Vérification si le mot de passe maître est défini
cursor.execute('SELECT password, key FROM master_password')
mdp_maitre_defini = cursor.fetchone()

# Définition du mot de passe maître
def definir_mot_de_passe_maitre():
    def sauvegarder_mot_de_passe_maitre():
        mot_de_passe = zone_mdp.get()
        mot_de_passe_confirme = zone_mdp_confirme.get()
        if mot_de_passe and mot_de_passe == mot_de_passe_confirme:
            key = generate_key()
            mot_de_passe_hache = hacher_mot_de_passe(mot_de_passe)
            mot_de_passe_chiffre = encrypt(mot_de_passe_hache, key)
            cursor.execute('INSERT INTO master_password (password, key) VALUES (?, ?)', (mot_de_passe_chiffre, key))
            conn.commit()
            messagebox.showinfo("Succès", "Mot de passe maître défini avec succès !")
            fenetre_mdp_maitre.destroy()
            afficher_fenetre_principale(key)
        else:
            messagebox.showwarning("Erreur", "Les mots de passe ne correspondent pas ou sont vides.")

    fenetre_mdp_maitre = tk.Tk()
    fenetre_mdp_maitre.title("Définir le mot de passe maître")
    fenetre_mdp_maitre.geometry("300x150")
    fenetre_mdp_maitre.configure(bg="#f0f0f0")

    tk.Label(fenetre_mdp_maitre, text="Entrez un mot de passe maître:", bg="#f0f0f0").pack(pady=5)
    zone_mdp = tk.Entry(fenetre_mdp_maitre, show='*', width=25)
    zone_mdp.pack(pady=5)

    tk.Label(fenetre_mdp_maitre, text="Confirmez le mot de passe:", bg="#f0f0f0").pack(pady=5)
    zone_mdp_confirme = tk.Entry(fenetre_mdp_maitre, show='*', width=25)
    zone_mdp_confirme.pack(pady=5)

    tk.Button(fenetre_mdp_maitre, text="Définir", command=sauvegarder_mot_de_passe_maitre, bg="#4caf50", fg="white").pack(pady=10)
    fenetre_mdp_maitre.mainloop()

# Connexion avec le mot de passe maître
def connexion():
    def verifier_mot_de_passe_maitre():
        mot_de_passe = zone_mdp.get()
        mot_de_passe_hache = hacher_mot_de_passe(mot_de_passe)
        cursor.execute('SELECT password, key FROM master_password')
        record = cursor.fetchone()
        if record:
            mot_de_passe_chiffre, key = record
            mot_de_passe_dechiffre = decrypt(mot_de_passe_chiffre, key)
            if mot_de_passe_hache == mot_de_passe_dechiffre:
                messagebox.showinfo("Succès", "Connexion réussie !")
                fenetre_connexion.destroy()
                afficher_fenetre_principale(key)
            else:
                messagebox.showwarning("Erreur", "Mot de passe incorrect.")
        else:
            messagebox.showwarning("Erreur", "Erreur lors de la récupération du mot de passe.")

    fenetre_connexion = tk.Tk()
    fenetre_connexion.title("Connexion")
    fenetre_connexion.geometry("300x150")
    fenetre_connexion.configure(bg="#f0f0f0")

    tk.Label(fenetre_connexion, text="Entrez le mot de passe maître:", bg="#f0f0f0").pack(pady=5)
    zone_mdp = tk.Entry(fenetre_connexion, show='*', width=25)
    zone_mdp.pack(pady=5)

    tk.Button(fenetre_connexion, text="Se connecter", command=verifier_mot_de_passe_maitre, bg="#4caf50", fg="white").pack(pady=10)
    fenetre_connexion.mainloop()

# Fenêtre principale
def afficher_fenetre_principale(key):
    root = tk.Tk()
    root.title("Gestionnaire de Mots de Passe")
    root.geometry("500x400")
    root.configure(bg="#f0f0f0")

    # Fonction pour ajouter une nouvelle entrée de mot de passe
    def ajouter_mot_de_passe():
        site = zone_site.get()
        pseudo = zone_pseudo.get()
        mdp = zone_mdp.get()
        if site and pseudo and mdp:
            mdp_chiffre = encrypt(mdp, key)
            cursor.execute('INSERT INTO passwords (site, pseudo, mdp) VALUES (?, ?, ?)', (site, pseudo, mdp_chiffre))
            conn.commit()
            messagebox.showinfo("Succès", "Mot de passe ajouté avec succès !")
            afficher_mots_de_passe()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

    # Fonction pour afficher les mots de passe
    def afficher_mots_de_passe():
        for widget in frame_mots_de_passe.winfo_children():
            widget.destroy()
        cursor.execute('SELECT site, pseudo, mdp FROM passwords')
        for index, (site, pseudo, mdp_chiffre) in enumerate(cursor.fetchall()):
            try:
                mdp = decrypt(mdp_chiffre, key)
                tk.Label(frame_mots_de_passe, text=f"{site} - {pseudo} - {mdp}", bg="#f0f0f0").grid(row=index, column=0, sticky="w")
            except:
                tk.Label(frame_mots_de_passe, text=f"{site} - {pseudo} - (Déchiffrement échoué)", bg="#f0f0f0").grid(row=index, column=0, sticky="w")

    # En-tête
    tk.Label(root, text="Gestionnaire de Mots de Passe", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)

    # Entrées pour ajouter un nouveau mot de passe
    entry_frame = tk.Frame(root, bg="#f0f0f0")
    entry_frame.pack(pady=10)

    tk.Label(entry_frame, text="Site:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    zone_site = tk.Entry(entry_frame, width=30)
    zone_site.grid(row=0, column=1, pady=5)

    tk.Label(entry_frame, text="Pseudo:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    zone_pseudo = tk.Entry(entry_frame, width=30)
    zone_pseudo.grid(row=1, column=1, pady=5)

    tk.Label(entry_frame, text="Mot de passe:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    zone_mdp = tk.Entry(entry_frame, show='*', width=30)
    zone_mdp.grid(row=2, column=1, pady=5)

    tk.Button(entry_frame, text="Ajouter", command=ajouter_mot_de_passe, bg="#4caf50", fg="white").grid(row=3, columnspan=2, pady=10)

    # Liste des mots de passe
    frame_mots_de_passe = tk.Frame(root, bg="#f0f0f0")
    frame_mots_de_passe.pack(pady=20)

    afficher_mots_de_passe()
    root.mainloop()

# Choix de l'interface à afficher
if mdp_maitre_defini is None:
    definir_mot_de_passe_maitre()
else:
    connexion()

# Fermer la connexion à la base de données lorsque l'application se ferme
conn.close()
