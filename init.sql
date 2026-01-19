-- ============================================================================
-- INIT.SQL - Initialisation de la base de données Bitcoin Prediction
-- ============================================================================
-- Projet: Plateforme de prédiction Bitcoin BTC/USDT
-- Database: PostgreSQL 14+
-- Architecture: Medallion (Bronze -> Silver -> Gold/Service)
-- ============================================================================

-- Création de la base de données
CREATE DATABASE bitcoin_prediction;

-- Création d'un utilisateur dédié à l'application
CREATE USER btc_user WITH PASSWORD 'btc_secure_password_2026';

-- Attribution des privilèges sur la base de données
GRANT ALL PRIVILEGES ON DATABASE bitcoin_prediction TO btc_user;

-- Attribution des droits sur le schéma public
GRANT ALL ON SCHEMA public TO btc_user;

-- Connexion à la base (à exécuter manuellement si nécessaire)
-- \c bitcoin_prediction

-- ============================================================================
-- SILVER LAYER (Structure initiale)
-- ============================================================================
-- Table temporaire : les colonnes seront ajoutées après la finalisation
-- du pipeline de Data Engineering (Bronze -> Silver)
-- ============================================================================

CREATE TABLE IF NOT EXISTS btc_cleaned (
    id SERIAL PRIMARY KEY
);
