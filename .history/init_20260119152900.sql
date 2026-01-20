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
CREATE TABLE btc_cleaned (
    id SERIAL PRIMARY KEY# =====================================
# Environment Variables Example File
# =====================================

# Hugging Face
HF_TOKEN=your_huggingface_token_here

# =====================================
# PostgreSQL Database Configuration
# =====================================
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

# =====================================
# JWT (JSON Web Token) Configuration
# =====================================
SK=your_secret_key_here
ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
);

