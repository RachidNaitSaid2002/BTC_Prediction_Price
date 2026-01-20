-- Créer la base de données
CREATE DATABASE taxi_nyc;

-- Créer un nouvel utilisateur
CREATE USER taxi_user WITH PASSWORD 'ton_mot_de_passe_securise';

-- Donner tous les droits sur la base taxi_nyc
GRANT ALL PRIVILEGES ON DATABASE taxi_nyc TO taxi_user;

-- Donner les droits sur le schéma public
GRANT ALL ON SCHEMA public TO taxi_user;

-- Table des utilisateurs pour l'authentification
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Index pour accélérer les recherches par username
CREATE INDEX idx_users_username ON users(username);
