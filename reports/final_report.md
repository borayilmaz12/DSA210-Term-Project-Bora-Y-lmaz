# DSA210 Final Report  
# League of Legends Ranked Match Outcome Analysis

## 1. Motivation

The goal of this project is to analyze ranked League of Legends match data and investigate which player performance factors are associated with winning or losing a match.

League of Legends is a competitive team-based game where match outcome can be influenced by many factors such as champion choice, role, mechanical performance, damage contribution, vision control, and player tier. Because the game produces detailed match-level statistics, it is a suitable domain for applying the full data science pipeline.

The main research questions of this project are:

1. Do winning matches have higher vision score than losing matches?
2. Do winning matches have higher vision per minute than losing matches?
3. Is player tier associated with match outcome?
4. Can match outcome be classified using performance-based features?
5. Which variables are most useful for explaining match outcomes?

This project applies data collection, data cleaning, exploratory data analysis, hypothesis testing, supervised machine learning, model evaluation, and interpretation.

---

## 2. Data Source and Collection

The dataset was collected using the Riot Games API. Each row in the processed dataset represents a player-level observation from a ranked League of Legends match.

The dataset includes variables such as:

- match outcome (`win`)
- player tier
- champion
- role
- kills
- deaths
- assists
- KDA
- damage
- vision score
- damage per minute
- vision per minute
- other per-minute performance features

The processed dataset is stored in:

`data/processed/lol_ranked_dataset.csv`

The project uses the processed version of the dataset for analysis and machine learning. API keys and private environment variables are not included in the repository.

---

## 3. Data Cleaning and Feature Engineering

Before conducting analysis, I inspected the dataset for missing values, inconsistent column names, and invalid values. I also checked the structure of the dataset to make sure that the variables were suitable for exploratory analysis, hypothesis testing, and machine learning.

The final machine learning dataset contained 2,980 observations and 8 selected predictive features:

- `kda`
- `damage_per_min`
- `vision_per_min`
- `kills`
- `deaths`
- `assists`
- `role`
- `champion`

There were no missing values in the selected machine learning features.

Feature engineering was important because raw totals can be affected by match duration. For example, a longer match naturally allows more time to deal damage, gain vision score, or farm minions. Therefore, per-minute features were used to make comparisons fairer across matches of different lengths.

Important engineered or derived features include:

- `kda`: a summary of kills, deaths, and assists
- `damage_per_min`: damage normalized by match duration
- `vision_per_min`: vision score normalized by match duration

Categorical variables such as `role` and `champion` were encoded for machine learning models.

---

## 4. Exploratory Data Analysis

The EDA was expanded based on earlier feedback. In addition to basic data inspection, I analyzed the dataset across several dimensions:

- win/loss distribution
- role-level performance
- champion-level performance
- damage and damage per minute
- vision score and vision per minute
- per-minute performance variables
- relationships among numerical variables

Role-level analysis helped examine whether average performance and win rate differed by position. Champion-level analysis helped identify whether certain champions were associated with stronger observed performance, although champion-specific results should be interpreted carefully when sample sizes are small.

Damage and damage-per-minute analysis helped evaluate offensive contribution. Vision score and vision-per-minute analysis helped evaluate map-awareness-related contribution. Per-minute features were especially important because they reduce the effect of match duration.

Overall, the EDA suggested that performance variables such as KDA, damage per minute, and vision-related metrics may differ between wins and losses. These patterns motivated the hypothesis testing and machine learning stages.

---

## 5. Hypothesis Testing

I performed hypothesis tests to evaluate whether the patterns observed during EDA were statistically meaningful.

### 5.1 Vision Score and Match Outcome

First, I tested whether winning matches have higher vision score than losing matches.

Because the research question was directional, I used a one-sided Welch independent samples t-test.

Let:

- μ_win = mean vision score in winning matches
- μ_loss = mean vision score in losing matches

Hypotheses:

- H0: μ_win ≤ μ_loss
- H1: μ_win > μ_loss

I reported the sample sizes, group means, standard deviations, test statistic, and one-sided p-value.

Result:

- p-value = 0.0123272285919966

Since p < 0.05, I reject H0 at α = 0.05.

This means that the data provide sufficient evidence that winning matches have higher vision score than losing matches.

### 5.2 Vision Per Minute and Match Outcome

Second, I repeated the same logic using vision per minute. This was important because raw vision score can be affected by match duration. By using vision per minute, I compared vision contribution in a more normalized way across games of different lengths.

Hypotheses:

- H0: μ_win_vpm ≤ μ_loss_vpm
- H1: μ_win_vpm > μ_loss_vpm

Result:

- p-value = 0.002268917738666885

Since p < 0.05, I reject H0 at α = 0.05.

This suggests that vision per minute is significantly higher in winning matches.

### 5.3 Player Tier and Match Outcome

Third, I used a chi-square test of independence to examine whether player tier and match outcome are associated.

Both variables are categorical:

- `tier`: player rank category
- `win`: match outcome

The chi-square test compares the observed win/loss counts across tiers with the expected counts under the assumption of independence.

Hypotheses:

- H0: Player tier and match outcome are independent.
- H1: Player tier and match outcome are not independent.

Result:

- p-value = 0.0037404149125206984

Since p < 0.05, I reject H0 at α = 0.05.

Therefore, the data provide sufficient evidence of an association between player tier and match outcome.

### 5.4 Hypothesis Testing Summary

Overall, the hypothesis tests connect the exploratory findings with statistical evidence. The results suggest that variables related to vision and player tier are associated with match outcomes.

However, these results should be interpreted carefully. Statistical association does not imply causation. The hypothesis tests show that there is evidence of relationships in the collected data, but they do not prove that vision score or tier directly causes a win.

These findings guided the machine learning stage by helping identify potentially useful predictive features such as vision score, vision per minute, tier, role, champion, damage, and per-minute performance variables.

---

## 6. Machine Learning Methods

The machine learning task was formulated as a binary classification problem.

Target variable:

- `win`

The goal was to classify whether a match was won or lost using performance-based features.

Features used included:

- KDA
- damage per minute
- vision per minute
- kills
- deaths
- assists
- role
- champion

I trained and evaluated the following models:

1. Baseline model
2. Logistic Regression
3. Decision Tree Classifier
4. k-Nearest Neighbors
5. Random Forest Classifier

The baseline model was used as a reference point. It predicts the majority class and helps show whether the machine learning models perform better than a naive approach.

The dataset was split into training and test sets:

- Training set size: 2,384 observations
- Test set size: 596 observations
- Train win rate: 0.50
- Test win rate: 0.50

The balanced win rate in both train and test sets shows that stratified splitting preserved the class distribution.

Numerical features were scaled, and categorical features were one-hot encoded. Scaling was especially important for kNN because distance-based algorithms are affected by feature scale.

---

## 7. Model Evaluation

Models were evaluated using multiple classification metrics:

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Confusion matrix

Accuracy alone was not enough because a model can achieve reasonable accuracy by predicting the majority class. Therefore, F1 score and ROC-AUC were also considered.

The baseline model produced 0.50 accuracy. Since the dataset was balanced, predicting only one class resulted in 50% accuracy. However, the baseline had precision, recall, and F1 score equal to 0 for the positive class, showing that it was not useful for identifying wins.

Model comparison:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Baseline | 0.5000 | 0.0000 | 0.0000 | 0.0000 | NaN |
| Logistic Regression | 0.8171 | 0.8436 | 0.7785 | 0.8098 | 0.9024 |
| Decision Tree | 0.8205 | 0.8866 | 0.7349 | 0.8037 | 0.8878 |
| kNN | 0.7768 | 0.7816 | 0.7685 | 0.7750 | 0.8391 |
| Random Forest | 0.8171 | 0.8621 | 0.7550 | 0.8050 | 0.8921 |

The best-performing model overall was Logistic Regression because it had the highest F1 score and the highest ROC-AUC among the tested models. Although the Decision Tree had slightly higher accuracy, Logistic Regression provided better balance between precision and recall and better ranking ability based on ROC-AUC.

The Logistic Regression confusion matrix was:

| Actual / Predicted | Predicted Loss | Predicted Win |
|---|---:|---:|
| Actual Loss | 255 | 43 |
| Actual Win | 66 | 232 |

This means the Logistic Regression model correctly classified 255 losses and 232 wins. It misclassified 43 losses as wins and 66 wins as losses.

The Decision Tree confusion matrix was:

| Actual / Predicted | Predicted Loss | Predicted Win |
|---|---:|---:|
| Actual Loss | 270 | 28 |
| Actual Win | 79 | 219 |

The kNN confusion matrix was:

| Actual / Predicted | Predicted Loss | Predicted Win |
|---|---:|---:|
| Actual Loss | 234 | 64 |
| Actual Win | 69 | 229 |

The Random Forest confusion matrix was:

| Actual / Predicted | Predicted Loss | Predicted Win |
|---|---:|---:|
| Actual Loss | 262 | 36 |
| Actual Win | 73 | 225 |

Overall, all supervised models performed substantially better than the baseline model.

---

## 8. Hyperparameter Tuning

I also tested the effect of model complexity for Decision Tree and kNN.

For the Decision Tree, I tested different values of `max_depth` from 1 to 10 using 5-fold cross-validation and F1 score. The best cross-validation F1 score was obtained around `max_depth = 4`, with mean CV F1 = 0.7969. This supports the use of a limited-depth tree because very deep trees can overfit the training data.

For kNN, I tested different odd values of `k` from 1 to 21 using 5-fold cross-validation and F1 score. The CV results improved as `k` increased, with the best tested value being `k = 21`, which reached mean CV F1 = 0.7957. This suggests that very small k values were more sensitive to noise, while larger k values produced more stable performance.

---

## 9. Feature Importance and Interpretation

To understand which variables were most useful for predicting match outcome, I examined Decision Tree feature importance and Logistic Regression coefficients.

The Decision Tree identified the following important features:

1. KDA
2. Damage per minute
3. Role_TOP
4. Role_JUNGLE
5. Vision per minute

The Decision Tree feature importance values showed that KDA was by far the most important feature, with importance 0.9503. This means that the tree relied heavily on KDA when separating wins from losses.

Other important Decision Tree features were:

- `damage_per_min`: 0.0183
- `role_TOP`: 0.0165
- `role_JUNGLE`: 0.0070
- `vision_per_min`: 0.0064
- `deaths`: 0.0015

Logistic Regression showed the strongest positive coefficients for:

1. champion_Karthus: 1.6554
2. KDA: 1.4296
3. Assists: 1.2672

Other strong positive coefficients included:

- champion_Elise: 1.2023
- champion_Senna: 0.9370
- kills: 0.8929
- champion_Pyke: 0.8637

The strongest negative coefficients were:

1. champion_Taric: -1.1404
2. champion_Jhin: -1.1235
3. champion_Galio: -1.0753

Other negative coefficients included:

- champion_Shen: -1.0295
- champion_JarvanIV: -1.0185
- champion_Soraka: -0.9775
- champion_Rakan: -0.9272
- deaths: -0.8737

The most consistent predictor across models was KDA. It appeared as the most important feature in the Decision Tree and also had a strong positive coefficient in Logistic Regression. This suggests that better kill/death/assist performance is strongly associated with winning.

Damage per minute and vision per minute were also important. These variables are useful because they normalize performance by match duration and allow fairer comparisons across games.

Role-related variables such as TOP and JUNGLE also appeared important in the Decision Tree, suggesting that the relationship between role and match outcome may vary across positions.

Champion-specific effects should be interpreted carefully because they may depend on sample size and champion frequency in the dataset. A champion may appear important if it occurs in a small number of matches or if it is strongly associated with a specific subset of the data.

Overall, the most reliable predictors were:

1. KDA
2. Damage per minute
3. Vision per minute
4. Role
5. Champion-specific effects

Because many of these variables are post-game performance statistics, the model should be interpreted as explaining match outcomes rather than predicting them before the match starts.

---

## 10. Main Findings

The main findings of this project are:

1. Winning matches had significantly higher vision score than losing matches.
2. Winning matches also had significantly higher vision per minute.
3. Player tier and match outcome were statistically associated.
4. Logistic Regression was the best overall model based on F1 score and ROC-AUC.
5. Decision Tree achieved the highest accuracy, but Logistic Regression had better F1 and ROC-AUC.
6. KDA was the most consistent and important predictor across models.
7. Damage per minute and vision per minute were important performance-based features.
8. Role-related variables provided useful predictive information.
9. Champion-specific variables affected the models, but these should be interpreted cautiously due to possible sample-size effects.
10. All supervised learning models performed substantially better than the baseline model.

Overall, the analysis suggests that match outcome is associated with both mechanical performance indicators and strategic contribution indicators such as vision.

---

## 11. Limitations

This project has several limitations.

First, many of the features used in the machine learning models are post-game performance variables. For example, KDA, damage per minute, and vision per minute are only known after or during a match. Therefore, the models should be interpreted as explaining which performance metrics are associated with winning rather than predicting the outcome before the game begins.

Second, champion-specific coefficients may be affected by sample size. If some champions appear only a small number of times, their coefficients or importance values may not generalize well.

Third, League of Legends is a team-based game, but the dataset mainly uses player-level observations. A player’s match outcome depends not only on their own performance but also on teammates, opponents, team composition, objectives, patch version, and in-game strategy.

Fourth, the data were collected through the Riot Games API, which may introduce limitations related to rate limits, sample selection, and available match history.

Fifth, the analysis shows statistical associations, not causation. For example, higher vision score is associated with winning, but this does not prove that increasing vision score alone directly causes wins.

Sixth, the machine learning models may partly capture post-match explanations rather than true pre-match prediction ability because several input features are only available after the match has been played.

---

## 12. Future Work

Future work could improve the project in several ways:

1. Collect a larger dataset from more players and more matches.
2. Analyze players separately by role.
3. Add team-level features such as objective control, towers, dragons, barons, and team gold difference.
4. Include patch/version information because champion strength and game balance change over time.
5. Separate pre-game prediction from post-game explanation.
6. Build a true pre-game prediction model using only features known before the match starts.
7. Use more systematic hyperparameter tuning for all models.
8. Compare model performance across different tiers.
9. Use additional models and ensemble methods.
10. Investigate champion-specific effects only for champions with sufficient sample sizes.
11. Build a dashboard or visualization page to communicate findings more clearly.

---

## 13. Conclusion

This project applied the full data science pipeline to ranked League of Legends match data. The project included data collection, data cleaning, exploratory data analysis, hypothesis testing, supervised machine learning, model evaluation, and interpretation.

The hypothesis tests showed that winning matches had significantly higher vision score and vision per minute than losing matches. They also showed that player tier and match outcome were statistically associated.

The machine learning results showed that Logistic Regression, Decision Tree, kNN, and Random Forest all performed better than the baseline model. Logistic Regression was the best overall model based on F1 score and ROC-AUC, while Decision Tree achieved the highest accuracy.

The most important features for explaining match outcomes were KDA, damage per minute, vision per minute, role, and champion-specific effects. KDA was the most consistent predictor across both Decision Tree and Logistic Regression.

Overall, the project shows how data science methods can be used to analyze competitive gameplay data and extract meaningful insights about performance factors associated with winning. However, because many variables are post-game statistics, the models should be interpreted as explanatory rather than as true pre-game prediction systems.