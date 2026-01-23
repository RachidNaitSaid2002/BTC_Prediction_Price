-- ============================================================================
-- INIT.SQL - Initialisation de la base de données Bitcoin Prediction
-- ============================================================================

-- Créer l'utilisateur pour l'API
CREATE USER btc_user WITH PASSWORD 'manal.2480';

-- Donner accès à la base airflow (partagée)
GRANT ALL PRIVILEGES ON DATABASE airflow TO btc_user;

-- Connexion à la base airflow
\c airflow

-- Attribution des droits sur le schéma public
GRANT ALL ON SCHEMA public TO btc_user;
GRANT ALL ON SCHEMA public TO airflow;

-- ============================================================================
-- TABLES POUR L'API
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bitcoin_predictions (
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
    user_id INTEGER REFERENCES users(id)
);

-- ============================================================================
-- TABLES POUR AIRFLOW/ML PIPELINE
-- ============================================================================

CREATE TABLE IF NOT EXISTS silver_data_test (
    id SERIAL PRIMARY KEY,
    open_time TIMESTAMP NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    close_time TIMESTAMP,
    quote_volume DOUBLE PRECISION,
    count INTEGER,  
    taker_buy_volume DOUBLE PRECISION,
    taker_buy_quote_volume DOUBLE PRECISION,
    taker_ratio DOUBLE PRECISION,
    ma_5 DOUBLE PRECISION, 
    ma_10 DOUBLE PRECISION, 
    prev_close DOUBLE PRECISION,
    return DOUBLE PRECISION,
    close_t_plus_10 DOUBLE PRECISION
);

-- Attribution des privilèges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO btc_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO airflow;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO btc_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO airflow;

-- Attribution automatique pour les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO btc_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO airflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO btc_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO airflow;