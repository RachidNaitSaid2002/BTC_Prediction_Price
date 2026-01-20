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

