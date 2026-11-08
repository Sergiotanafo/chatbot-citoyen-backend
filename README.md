# Chatbot Citoyen Malien — Backend

## 1. Présentation du projet

Ce dépôt contient le backend du **Chatbot Citoyen Malien**.

Le backend constitue la couche centrale de gestion des échanges entre les interfaces frontend, les services métier, la base de données et le moteur d'intelligence artificielle (DSP).

## 2. Objectifs

- Exposer les fonctionnalités du système à travers une API REST.
- Gérer les utilisateurs et leurs accès.
- Traiter les requêtes provenant du frontend.
- Assurer la gestion et la persistance des données.
- Communiquer avec le DSP à travers gRPC.

## 3. Architecture du backend

L'architecture repose sur plusieurs composants :

- **API :** gestion des routes et des requêtes HTTP.
- **Services :** implémentation de la logique métier.
- **Repositories :** accès aux données.
- **Schemas :** validation et structuration des données.
- **Security :** authentification et autorisations.
- **Clients :** communication avec les services externes.
- **Migrations :** gestion de l'évolution de la base de données.

## 4. Technologies

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy (à confirmer)
- Alembic (à confirmer)
- gRPC et Protocol Buffers

## 5. Fonctionnalités prévues

- Gestion des utilisateurs.
- Authentification et autorisation.
- Gestion des conversations.
- Gestion des informations et contenus citoyens.
- Communication avec le moteur DSP.
- Accès et gestion des données PostgreSQL.

## 6. Installation

Les instructions détaillées seront complétées après la mise en place de l'environnement Python et des dépendances.

## 7. Configuration

La configuration reposera notamment sur des variables d'environnement pour :
- La connexion PostgreSQL.
- Les paramètres de sécurité.
- Les adresses des services.
- La communication gRPC avec le DSP.

Les secrets ne doivent jamais être publiés dans le dépôt.

## 8. API

La documentation interactive de l'API sera accessible via Swagger (`/docs`) lorsque le serveur sera démarré.

## 9. Tests

Les tests automatisés permettront de vérifier les routes API, les services et les interactions avec les autres composants.

## 10. Collaboration

Les contributions sont réalisées à travers des branches Git et des Pull Requests.

## 11. État du projet

Projet en cours de développement.

## 12. Équipe

Projet : Chatbot Citoyen Malien.
