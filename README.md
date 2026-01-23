# BTC Prediction Platform

![Image](https://via.placeholder.com/800x400.png?text=BTC+Prediction+Platform)
![Image](https://via.placeholder.com/800x400.png?text=Architecture+Diagram)
![Image](https://via.placeholder.com/800x400.png?text=Data+Pipeline)
![Image](https://via.placeholder.com/800x400.png?text=Machine+Learning+Results)

## Table des Matières

- [BTC Prediction Platform](#btc-prediction-platform)
  - [Table des Matières](#table-des-matières)
  - [Contexte du Projet](#contexte-du-projet)
    - [Problématique](#problématique)
    - [Objectifs](#objectifs)
    - [Solution](#solution)
  - [Architecture](#architecture)
    - [Architecture Globale](#architecture-globale)
    - [Workflow de Prédiction](#workflow-de-prédiction)
  - [Technologies Utilisées](#technologies-utilisées)
    - [Data Engineering \& Orchestration](#data-engineering--orchestration)
    - [Machine Learning](#machine-learning)
    - [Backend \& API](#backend--api)
  - [Installation (Docker)](#installation-docker)
  - [Structure du Projet](#structure-du-projet)

## Contexte du Projet

### Problématique
Dans le secteur de la Fintech et des hedge funds, la capacité à traiter des flux de données massifs en temps réel pour anticiper les mouvements de marché est un avantage concurrentiel majeur. La société Quant-AI, spécialisée en analyse algorithmique, souhaite valider un prototype de plateforme prédictive.

Les traders et outils d'aide à la décision manquent actuellement d'une source de données centralisée et traitée capable de fournir une vision prédictive à court terme (T+10 minutes).

### Objectifs
Le défi consiste à bâtir une chaîne de valeur complète de la donnée qui répond aux contraintes suivantes :

- **Latence** : Ingestion et traitement rapide des flux de l'API Binance
- **Scalabilité** : Utilisation de technologies de calcul distribué pour gérer l'historique croissant
- **Fiabilité** : Automatisation des pipelines via une orchestration rigoureuse
- **Sécurité** : Protection de la propriété intellectuelle via un accès contrôlé

### Solution
BTC Prediction Platform automatise la collecte, le traitement distribué et l'exposition de prédictions financières via une architecture robuste et sécurisée.

La plateforme suit une logique de montée en qualité :

- **Zone Bronze** : Données brutes issues de Binance
- **Zone Silver** : Données nettoyées, typées et enrichies d'indicateurs via PySpark
- **Service Layer** : Modèles de régression et API de consultation

## Architecture

### Architecture Globale

┌─────────────────────────────────────────────────────────────────┐
│ Client / Frontend                                                │
│ (Dashboard / API Calls)                                          │
└────────────────┬───────────────────────────────────────────────┘
                 │ HTTP/REST + JWT
┌────────────────▼────────────────────────────────────────────────┐
│ FastAPI Backend                                                   │
│ (Port 8000)                                                       │
│ • Authentication (JWT)                                           │
│ • Prediction Endpoints                                           │
│ • Analytics Endpoints                                            │
│ • Model Serving                                                  │
└────────┬───────────────────────────┬────────────────────────────┘
         │                           │
┌────────▼───────────────┐  ┌───────▼─────────────────────────────┐
│ PostgreSQL DB           │  │ Apache Airflow                      │
│ • silver_data_test      │  │ (Orchestration)                    │
│ • users                 │  │ DAG ETL_TASKFLOW (15 min)          │
│ • predictions           │  │ DAG ml_pipeline (10 min)           │
└────────────────────────┘  └────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ PySpark Processing                           │
│ • Feature Engineering                       │
│ • Data Cleaning                             │
│ • Distributed Computing                    │
└────────────────────────────────────────────┘

### Workflow de Prédiction
┌──────────────┐
│ Binance API  │ (OHLC – 1 min)
└──────┬───────┘
       │ Extraction
┌──────▼────────────────┐
│ DAG ETL_TASKFLOW      │
└──────┬────────────────┘
       │ Bronze (Parquet)
┌──────▼────────────────┐
│ Zone Bronze           │
└──────┬────────────────┘
       │ PySpark Transform
┌──────▼────────────────────────────┐
│ Feature Engineering                │
│ MA_5, MA_10, return, taker_ratio  │
│ close_t_plus_10 (target)          │
└──────┬────────────────────────────┘
       │ Silver (Parquet)
┌──────▼────────────────┐
│ Zone Silver           │
└──────┬────────────────┘
       │ PostgreSQL
┌──────▼─────────────────┐
│ silver_data_test       │
└────────────────────────┘
       │
┌──────▼─────────────────────────────┐
│ DAG ml_pipeline                     │
│ Train + Evaluate Models             │
└──────┬─────────────────────────────┘
       │
┌──────▼────────────────┐
│ FastAPI /predict      │
└───────────────────────┘

## Technologies Utilisées

### Data Engineering & Orchestration
| Technologie | Version | Usage |
|------------|---------|-------|
| Apache Airflow | 2.8.1 | Orchestration ETL & ML |
| PySpark | 3.5.0 | Traitement distribué |
| PostgreSQL | 13+ | Base relationnelle |
| Docker | Latest | Containerisation |

### Machine Learning
| Technologie | Usage |
|------------|-------|
| Linear Regression | Baseline |
| Random Forest | Modèle principal |
| Gradient Boosting Trees | Boosting |

### Backend & API
| Technologie | Usage |
|------------|-------|
| FastAPI | API REST |
| JWT | Sécurité |
| SQLAlchemy | ORM |

## Installation (Docker)

```bash
git clone https://github.com/votre-username/BTC_Prediction_Price.git
cd BTC_Prediction_Price
docker-compose up -d --build
```

Airflow : http://localhost:8080
Backend : http://localhost:8000

## Structure du Projet

```bash
BTC_PREDICTION_PRICE/
├── airflow/                        # Orchestration des pipelines
│   ├── dags/                       # Définition des Workflows
│   │   ├── ETL.py                  # Pipeline d'extraction et transformation
│   │   └── ml_pipeline.py          # Pipeline d'entraînement/prédiction
│   ├── data/                       # Stockage géré par Airflow
│   │   ├── Bronze/                 # Données brutes (Raw)
│   │   └── Silver/                 # Données nettoyées/filtrées
│   ├── jars/                       # Dépendances Java (si utilisation de Spark)
│   ├── logs/                       # Logs d'exécution d'Airflow
│   ├── plugins/utils/              # Extensions et scripts utilitaires
│   │   └── fetch_api.py            # Script de récupération des données API
│   ├── utils/                      # Scripts d'aide généraux
│   ├── Dockerfile                  # Configuration Docker spécifique Airflow
│   └── init_airflow.sh             # Script d'initialisation de l'instance
├── backend/                        # API et logique serveur (FastAPI/Flask)
│   └── app/                        # (Contenu détaillé précédemment : auth, routes, etc.)
├── ml/                             # Science des données et Recherche
│   ├── Data/                       # Jeux de données pour l'entraînement
│   │   ├── Bronze/                 # Données historiques brutes
│   │   └── Silver/                 # Données prêtes pour le modèle
│   ├── Data_Engineer/              # Scripts de préparation hors Airflow
│   └── Machine Learning/notebooks/ # Expérimentation
│       ├── main.ipynb              # Notebook principal de recherche
│       └── __init__.py
├── venv/                           # Environnement virtuel Python
├── .env                            # Variables d'environnement
├── .env.example                    # Modèle de configuration
├── .gitignore                      # Fichiers ignorés par Git
├── docker-compose.yml              # Orchestration multi-conteneurs
├── init.sql                        # Script de base de données
├── README.md                       # Documentation du projet
└── requirements.txt                # Dépendances Python globales
```

