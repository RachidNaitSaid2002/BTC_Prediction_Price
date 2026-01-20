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

silver_btc_features

CREATE TABLE btc_raw (
    id SERIAL PRIMARY KEY,
    open_time BIGINT NOT NULL,
    open_price DOUBLE PRECISION NOT NULL,
    high_price DOUBLE PRECISION NOT NULL,
    low_price DOUBLE PRECISION NOT NULL,
    close_price DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL,
    close_time BIGINT NOT NULL,
    quote_asset_volume DOUBLE PRECISION,
    number_of_trades INTEGER,
    taker_buy_base_volume DOUBLE PRECISION,
    taker_buy_quote_volume DOUBLE PRECISION,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(open_time)
);
