# DSA210 Project - League of Legends Ranked Match Analysis

This project analyzes ranked League of Legends match data collected through the Riot Games API.

## Project Goal
The goal is to investigate how player and match-related features such as KDA, vision score, damage, role, and tier are associated with match outcomes.

## Structure
- `src/`: Python scripts for data collection
- `data/`: raw and processed datasets
- `notebooks/`: analysis notebooks

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