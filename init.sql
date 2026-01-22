-- ============================================================================
-- INIT.SQL - Initialisation de la base de données Bitcoin Prediction
-- ============================================================================

-- Création de la base de données
CREATE DATABASE bitcoin_prediction;

-- Création d'un utilisateur dédié à l'application
CREATE USER btc_user WITH PASSWORD 'manal.2480';

-- Attribution des privilèges sur la base de données
GRANT ALL PRIVILEGES ON DATABASE bitcoin_prediction TO btc_user;

-- Connexion à la base
\c bitcoin_prediction

-- Attribution des droits sur le schéma public
GRANT ALL ON SCHEMA public TO btc_user;

-- ============================================================================
-- SILVER LAYER (Structure initiale)
-- ============================================================================

CREATE TABLE IF NOT EXISTS btc_cleaned (
    id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Vérifier si la table existe et la supprimer
DROP TABLE IF EXISTS bitcoin_predictions CASCADE;

-- Recréer la table avec le bon schéma
CREATE TABLE bitcoin_predictions (
    id SERIAL PRIMARY KEY,
    
    "MA_5" DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION NOT NULL,
    low DOUBLE PRECISION NOT NULL,
    open DOUBLE PRECISION NOT NULL,
    close DOUBLE PRECISION NOT NULL,
    "MA_10" DOUBLE PRECISION NOT NULL,
    prev_close DOUBLE PRECISION NOT NULL,
    return_val DOUBLE PRECISION NOT NULL,
    predicted_price DOUBLE PRECISION NOT NULL,

    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

-- Attribution des privilèges sur les tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO btc_user;

-- FIX: Attribution des privilèges sur les séquences
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO btc_user;

-- Attribution automatique des privilèges pour les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL ON TABLES TO btc_user;

-- Attribution automatique des privilèges pour les futures séquences
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT USAGE, SELECT ON SEQUENCES TO btc_user;