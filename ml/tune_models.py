"""
Hyperparameter Tuning Module using GridSearchCV / RandomizedSearchCV
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

def tune_random_forest(X_train, y_train, cv=3, random_state=42):
    """
    Performs systematic GridSearchCV hyperparameter tuning on Random Forest Classifier.
    Demonstrates tuning parameter space: n_estimators, max_depth, min_samples_split.
    """
    param_grid = {
        "n_estimators": [50, 100],
        "max_depth": [10, 20, None],
        "min_samples_split": [2, 5]
    }
    rf = RandomForestClassifier(random_state=random_state)
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=cv,
        scoring="accuracy",
        n_jobs=1,
        verbose=0
    )
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_

def tune_decision_tree(X_train, y_train, cv=3, random_state=42):
    """
    Performs GridSearchCV on Decision Tree Classifier.
    """
    param_grid = {
        "max_depth": [3, 5, 8, None],
        "min_samples_split": [2, 5],
        "criterion": ["gini", "entropy"]
    }
    dt = DecisionTreeClassifier(random_state=random_state)
    grid_search = GridSearchCV(
        estimator=dt,
        param_grid=param_grid,
        cv=cv,
        scoring="accuracy",
        n_jobs=1,
        verbose=0
    )
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_
