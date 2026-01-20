-- ============================================================================
-- INIT.SQL - Initialisation de la base de données Bitcoin Prediction
-- ============================================================================
-- Projet: Plateforme de prédiction Bitcoin BTC/USDT
-- Database: PostgreSQL 14+
-- Architecture: Medallion (Bronze -> Silver -> Gold/Service)
-- ============================================================================



-- Créer la base de données
CREATE DATABASE bitcoin_prediction;

-- Créer un utilisateur pour l'application
CREATE USER btc_user WITH PASSWORD 'btc_secure_password_2026';

-- Donner tous les droits sur la base bitcoin_prediction
GRANT ALL PRIVILEGES ON DATABASE bitcoin_prediction TO btc_user;

-- Donner les droits sur le schéma public
GRANT ALL ON SCHEMA public TO btc_user;

-- Se connecter à la base de données (à faire manuellement si nécessaire)
-- \c bitcoin_prediction

--------------------    
silver_btc_features

CREATE TABLE silver_btc_features (
    id SERIAL PRIMARY KEY,
    

);

-- Index pour les requêtes temporelles
CREATE INDEX idx_btc_raw_open_time ON btc_raw(open_time);
CREATE INDEX idx_btc_raw_close_time ON btc_raw(close_time);
