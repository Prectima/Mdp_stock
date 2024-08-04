# Gestionnaire de Mots de Passe

Ce projet est la deuxième partie d'une série d'exercices de programmation en Python. Il s'agit d'une application de gestion de mots de passe avec une interface graphique, qui permet de stocker de manière sécurisée des identifiants pour différents sites. Le gestionnaire de mots de passe utilise le chiffrement pour protéger les données sensibles.

## Fonctionnalités

- **Mot de passe maître** : Utilisez un mot de passe maître pour accéder à l'application. Si le mot de passe maître n'est pas défini, l'utilisateur sera invité à le définir lors du premier lancement.
- **Chiffrement des mots de passe** : Les mots de passe des utilisateurs sont chiffrés avec la bibliothèque `cryptography` pour garantir leur sécurité.
- **Stockage sécurisé** : Les mots de passe, ainsi que les sites associés et les noms d'utilisateur, sont stockés dans une base de données SQLite.
- **Interface graphique** : L'application utilise Tkinter pour offrir une interface utilisateur intuitive et agréable.

## Prérequis

Avant de lancer l'application, assurez-vous d'avoir installé les bibliothèques suivantes :

- Python 3
- Tkinter (généralement inclus avec Python)
- `cryptography` : Vous pouvez l'installer via pip
pip install cryptography

## Installation

1. Clonez ce dépôt ou téléchargez le code source.
2. Assurez-vous d'avoir les prérequis installés.
3. Exécutez le fichier `main.py` pour lancer l'application.

## Utilisation

### Première Utilisation

1. Lors de la première utilisation, l'application vous demandera de définir un mot de passe maître. Ce mot de passe est crucial car il protégera tous vos mots de passe stockés.
2. Une fois le mot de passe maître défini, vous pourrez ajouter, afficher et gérer vos mots de passe.

### Connexion

1. Lors des connexions suivantes, entrez le mot de passe maître pour accéder à l'application.
2. Si le mot de passe est correct, vous serez dirigé vers l'interface principale où vous pourrez gérer vos mots de passe.

### Gestion des Mots de Passe

1. **Ajouter un mot de passe** : Remplissez les champs "Site", "Pseudo" et "Mot de passe", puis cliquez sur "Ajouter".
2. **Voir les mots de passe** : Les mots de passe seront listés dans la fenêtre principale.

## Sécurité

- **Chiffrement** : Les mots de passe sont chiffrés avec une clé générée aléatoirement à l'aide de la bibliothèque `cryptography`.
- **Hachage** : Le mot de passe maître est haché pour protéger l'accès à la base de données.

## Contribution

Les contributions sont les bienvenues ! Si vous souhaitez améliorer le projet, n'hésitez pas à ouvrir une pull request.

## Avertissements

- **Sécurité des données** : Ce projet est un exercice de programmation. Pour une utilisation en production, des mesures de sécurité supplémentaires doivent être implémentées, telles que le stockage sécurisé de la clé de chiffrement, la gestion des sessions, et des audits de sécurité.

## Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d'informations.
