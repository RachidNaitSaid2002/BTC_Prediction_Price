# BTC Prediction Platform

Platform de prédiction du prix du Bitcoin utilisant Apache Airflow, PySpark et Machine Learning pour automatiser l'ingestion, le traitement et la prédiction des données de marché en temps réel.

## Table des Matières

- [Vue d'ensemble](#vue-densemble)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Installation](#installation)
- [Structure du Projet](#structure-du-projet)
- [Pipelines](#pipelines)
- [API](#api)

## Vue d'ensemble

### Problématique

Les traders et hedge funds nécessitent une source centralisée de données traitées capable de fournir des prédictions à court terme (T+10 minutes) avec une latence minimale.

### Solution

Architecture automatisée suivant la méthodologie Medallion :

- **Bronze Layer** : Données brutes collectées depuis l'API Binance
- **Silver Layer** : Données nettoyées et enrichies avec indicateurs techniques
- **Gold Layer** : Modèles ML et prédictions exposées via API REST

### Fonctionnalités

- Collecte automatique des données OHLC (1 minute) depuis Binance
- Traitement distribué avec PySpark
- Entraînement automatique de modèles ML toutes les 15 minutes
- API REST sécurisée (JWT) pour les prédictions
- Orchestration complète via Apache Airflow

## Architecture

### Diagramme Global
```
┌─────────────┐
│ Binance API │
└──────┬──────┘
       │
┌──────▼────────────┐
│  Airflow ETL      │  (Toutes les 15 min)
│  - Extract        │
│  - Transform      │
│  - Load           │
└──────┬────────────┘
       │
┌──────▼───────────┐
│ PostgreSQL       │
│ silver_data_test │
└──────┬───────────┘
       │
┌──────▼─────────────┐
│ Airflow ML         │  (Toutes les 15 min)
│ - Train Models     │
│ - Evaluate         │
└──────┬─────────────┘
       │
┌──────▼────────┐
│  FastAPI      │
│  /predict     │
│  /analytics   │
└───────────────┘
```

### Flux de Données
```
Binance API → Bronze (Parquet) → PySpark Transform → Silver (Parquet) → PostgreSQL → ML Models → API
```

## Technologies

### Data Engineering

| Technologie | Version | Usage |
|------------|---------|-------|
| Apache Airflow | 2.8.1 | Orchestration ETL et ML |
| Apache Spark | 3.5.0 | Traitement distribué |
| PostgreSQL | 13+ | Base de données relationnelle |
| Docker Compose | Latest | Containerisation |

### Machine Learning

- Linear Regression (Baseline)
- Random Forest (Production)
- Gradient Boosting Trees (Expérimental)

### Backend

- FastAPI (API REST)
- JWT (Authentication)
- SQLAlchemy (ORM)

## Installation

### Prérequis

- Docker & Docker Compose
- 4GB RAM minimum
- Clé API Binance (optionnel pour données historiques)

### Démarrage Rapide
```bash
# Cloner le repository
git clone https://github.com/votre-username/BTC_Prediction_Price.git
cd BTC_Prediction_Price

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# Lancer l'infrastructure
docker-compose up -d --build

# Vérifier les services
docker-compose ps
```

### Accès aux Services

- Airflow UI: http://localhost:8080 (admin/admin)
- FastAPI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

## Structure du Projet
```
BTC_PREDICTION_PRICE/
├── .history/                       # Historique des fichiers (VS Code)
├── airflow/                        # Orchestration des flux de données
│   ├── dags/                       # Workflows Python
│   │   ├── ETL.py                  # Pipeline d'extraction et de chargement
│   │   └── ml_pipeline.py          # Pipeline de Machine Learning
│   ├── data/                       # Stockage des données par étapes
│   │   ├── Bronze/                 # Données brutes
│   │   ├── Silver/                 # Données transformées
│   │   ├── models/                 # Stockage des modèles entraînés
│   │   └── temp/                   # Fichiers temporaires de calcul
│   ├── logs/                       # Journaux d'exécution d'Airflow
│   ├── plugins/utils/              # Utilitaires pour les plugins Airflow
│   │   └── fetch_api.py            # Script de récupération des données API
│   ├── utils/                      # Scripts d'aide (Dockerfile, init_airflow.sh)
│   └── jars/                       # Librairies Java tierces
├── backend/                        # Partie Serveur / API
│   └── app/                        # Application principale
│       ├── auth/                   # Sécurité et Jetons
│       │   └── token_auth.py       # Gestion des tokens JWT
│       ├── core/                   # Configuration de base
│       │   └── config.py           # Variables globales
│       ├── db/                     # Connexion base de données
│       │   └── db_connection.py    # Logique de connexion SQL
│       ├── routes/                 # Endpoints de l'API
│       │   ├── prediction_router.py# Route pour les prévisions de prix
│       │   └── register_router.py  # Route pour l'inscription utilisateur
│       ├── schemas/                # Modèles de validation Pydantic
│       │   ├── LoginRequest_schema.py      # Validation connexion
│       │   ├── PredictionRequest_schema.py # Validation requête prédiction
│       │   └── Token_schema.py             # Structure du token
│       ├── services/               # Logique métier
│       │   └── prediction_service.py # Traitement des prédictions
│       ├── main.py                 # Entrée de l'application
│       └── Dockerfile              # Image Docker du backend
├── ml/                             # Recherche et Développement ML
│   ├── Data/                       # Datasets locaux (Bronze/Silver)
│   ├── Data_Engineer/              # Ingénierie des données
│   │   ├── Api_integration/        # Intégration des sources externes
│   │   └── Notebooks/              # Travaux de data engineering
│   └── Machine Learning/           # Modélisation
│       ├── model/                  # Fichiers de modèles sérialisés
│       └── notebooks/              # Expérimentations (main.ipynb)
├── venv/                           # Environnement virtuel Python
├── .env.example                    # Modèle de configuration
├── .gitignore                      # Fichiers à ignorer par Git
├── docker-compose.yml              # Orchestration totale du projet
├── init.sql                        # Initialisation de la base de données
├── README.md                       # Documentation
└── requirements.txt                # Dépendances Python
```

## Pipelines

### ETL Pipeline (ETL_TASKFLOW)

**Schedule**: Toutes les 15 minutes

**Workflow**:
```
extract → transform → save_silver_postgres
```

**Transformations**:
- Nettoyage des valeurs nulles
- Calcul de moyennes mobiles (MA_5, MA_10)
- Ratio taker/maker volume
- Target close_t_plus_10

### ML Pipeline (ml_pipeline)

**Schedule**: Toutes les 15 minutes (après ETL)

**Workflow**:
```
wait_for_etl → load_data → prepare_data → train_random_forest → evaluate_random_forest
```

**Features**:
- MA_5, MA_10
- high, low, open, close
- prev_close, return

**Target**: close_t_plus_10 (prix dans 10 minutes)

## API

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "username", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "username", "password": "password123"}'
```

### Predictions
```bash
# Get prediction
curl -X GET http://localhost:8000/predict \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Endpoints Disponibles

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | Créer un compte |
| `/auth/login` | POST | Obtenir un token JWT |
| `/predict` | GET | Obtenir une prédiction |
| `/analytics` | GET | Métriques du modèle |


## Configuration

### Variables d'Environnement
```bash
# PostgreSQL
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow

# FastAPI
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Développement

### Ajouter un nouveau DAG

1. Créer un fichier dans `airflow/dags/`
2. Définir le DAG avec `schedule_interval`
3. Le scheduler le détectera automatiquement

### Tester localement
```bash
# Tester l'ETL
docker-compose exec airflow-scheduler airflow dags test ETL_TASKFLOW 2026-01-23

# Tester le ML pipeline
docker-compose exec airflow-scheduler airflow dags test ml_pipeline 2026-01-23
```

### Monitoring
```bash
# Logs Airflow
docker-compose logs -f airflow-scheduler

# Logs FastAPI
docker-compose logs -f backend

# État des services
docker-compose ps
```

## Troubleshooting

### Le DAG ne démarre pas
```bash
# Vérifier les erreurs
docker-compose logs airflow-scheduler

# Relancer Airflow
docker-compose restart airflow-scheduler
```

### Problème de connexion PostgreSQL
```bash
# Vérifier que PostgreSQL est up
docker-compose ps postgres

# Tester la connexion
docker-compose exec postgres psql -U airflow -d airflow
```


