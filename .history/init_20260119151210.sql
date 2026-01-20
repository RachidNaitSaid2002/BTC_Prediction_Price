-- ============================================================================
-- INIT.SQL - Initialisation de la base de données Bitcoin Prediction
-- ============================================================================
-- Projet: Plateforme de prédiction Bitcoin BTC/USDT
-- Database: PostgreSQL 14+
-- Architecture: Medallion (Bronze -> Silver -> Gold/Service)
-- ============================================================================

-- Création du schéma principal
-- ============================================================================
-- Schéma Silver : Données nettoyées et enrichies
CREATE SCHEMA IF NOT EXISTS silver;

-- Schéma ML : Modèles et prédictions
CREATE SCHEMA IF NOT EXISTS ml;

-- Schéma Auth : Gestion des utilisateurs et authentification
CREATE SCHEMA IF NOT EXISTS auth;

COMMENT ON SCHEMA bronze IS 'Zone Bronze - Données brutes de l''API Binance';
COMMENT ON SCHEMA silver IS 'Zone Silver - Données nettoyées et features engineering';
COMMENT ON SCHEMA ml IS 'Zone Service - Modèles ML et prédictions';
COMMENT ON SCHEMA auth IS 'Gestion de l''authentification et des utilisateurs';