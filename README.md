# DSA210 Project - League of Legends Ranked Match Analysis

This project analyzes ranked League of Legends match data collected through the Riot Games API.

## Project Goal
The goal is to investigate how player and match-related features such as KDA, vision score, damage, role, and tier are associated with match outcomes.

## Structure
- `src/`: Python scripts for data collection
- `data/`: raw and processed datasets
- `notebooks/`: analysis notebooks

## How to Run

1. Create a .env file with your Riot API key:
   RIOT_API_KEY=your_key_here
   PLATFORM_REGION=euw1
   REGIONAL_ROUTING=europe

2. Install dependencies:
   pip install -r requirements.txt

3. Run scripts in order:
   - src/get_leaderboard.py
   - src/get_match_ids.py
   - src/get_match_data.py

4. Open notebooks/eda.ipynb for analysis.

## EDA and Hypothesis Testing

Exploratory Data Analysis (EDA) was conducted to examine distributions and relationships between variables such as kills, KDA, vision score, and damage.

Statistical hypothesis tests were performed:
- T-test to compare vision scores between winning and losing matches
- Chi-square test to evaluate the relationship between player tier and match outcome

## Data Source: Riot Games API  
https://developer.riotgames.com/apis

## Methodology
- Data collection from leaderboard players
- Data preprocessing and feature engineering
- Exploratory Data Analysis
- Hypothesis testing

## Data Preprocessing

Missing values were checked and handled appropriately. 
Duplicate entries were removed. 
Additional features such as KDA and per-minute statistics were computed to enrich the dataset.

## Milestone 1
This milestone includes:
- data collection from Riot API
- processed dataset construction
- EDA
- hypothesis testing
- revised project proposal

## Milestone 2: Machine Learning Methods

For the May 5 milestone, I expanded the analysis based on the previous feedback and applied supervised machine learning methods to predict match outcome.

### Improvements after feedback
- Added role-level EDA
- Added champion-level EDA
- Added damage and damage-per-minute analysis
- Added per-minute features to control for game duration
- Improved hypothesis test interpretation with sample sizes, assumptions, and one-sided directional testing

### Machine Learning Models
The target variable is `win`, representing match outcome.

Models used:
- Logistic Regression
- Decision Tree Classifier
- k-Nearest Neighbors
- Random Forest Classifier (optional/bonus)

### Evaluation Metrics
Models were evaluated using:
- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Confusion matrix

