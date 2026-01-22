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

CREATE TABLE IF NOT EXISTS bitcoin_predictions (
    id SERIAL PRIMARY KEY,

    ma_5 FLOAT NOT NULL,
    high FLOAT NOT NULL,
    low FLOAT NOT NULL,
    open FLOAT NOT NULL,
    close FLOAT NOT NULL,
    ma_10 FLOAT NOT NULL,
    prev_close FLOAT NOT NULL,
    return_val FLOAT NOT NULL,
    predicted_price FLOAT NOT NULL,

    user_id INTEGER REFERENCES users(id)

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