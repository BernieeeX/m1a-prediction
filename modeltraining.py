mkdir model
import os
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import (
    roc_auc_score, matthews_corrcoef, precision_recall_curve, auc, roc_curve,
    f1_score, accuracy_score  # Import f1_score and accuracy_score
)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib
import joblib
import numpy as np

mod_folder = '/home/share/shenglun/workspace/m1apre/data_moddivide/'
unmod_folder = '/home/share/shenglun/workspace/m1apre/data_unmoddivide/'
output_dir = '/home/share/shenglun/workspace/m1apre/model_xgboost/model/'
evaluation_dir = '/home/share/shenglun/workspace/m1apre/model_xgboost/evaluation/'
plot_folder = '/home/share/shenglun/workspace/m1apre/model_xgboost/plot/'

all_aucs = []
all_auprs = []
all_mccs = []
all_f1_scores = []  # Initialize a list for F1 Scores
all_accuracies = []  # Initialize a list for Accuracy Scores
processed_files = set()

for csv_file in os.listdir(mod_folder):
    if csv_file.endswith(".csv"):
        
        mod_file = os.path.join(mod_folder, csv_file)
        mod_data = pd.read_csv(mod_file)
        
        
        unmod_file = os.path.join(unmod_folder, csv_file.replace("_mod", "_unmod"))
        if not os.path.exists(unmod_file):
            print(f"Unmod file not found for {csv_file}. Skipping...")
            continue

        unmod_data = pd.read_csv(unmod_file)

        # feature
        X_mod = mod_data.iloc[:, 6:21].astype(float).values
        y_mod = pd.Series([1] * len(X_mod))

        X_unmod = unmod_data.iloc[:, 6:21].astype(float).values
        y_unmod = pd.Series([0] * len(X_unmod))

        # combine
        X = pd.concat([pd.DataFrame(X_mod), pd.DataFrame(X_unmod)], ignore_index=True)
        y = pd.concat([y_mod, y_unmod], ignore_index=True)

        # divide
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4, shuffle=True)

        # train xgboost
        clf = XGBClassifier(
            n_jobs=-1,
            learning_rate=0.1,
            n_estimators=500,
            alpha=0,
            gamma=0,
            reg_lambda=1,
            min_child_weight=1,
            max_depth=8,
            colsample_bytree=0.8,
            subsample=0.8,
            objective="binary:logistic"
        )
        clf.fit(X_train, y_train)

        # text
        y_pred = clf.predict(X_test)
        y_pred_prob = clf.predict_proba(X_test)[:, 1]

        # ROC FPR TPR
        fpr, tpr, _ = roc_curve(y_test, y_pred_prob)

        # AUC
        auc_score = auc(fpr, tpr)

        # Precision and Recall
        precision, recall, _ = precision_recall_curve(y_test, y_pred_prob)
        aupr_score = auc(recall, precision)

        # MCC
        mcc = matthews_corrcoef(y_test, y_pred)

        # Calculate F1 Score
        f1 = f1_score(y_test, y_pred)

        # Calculate Accuracy
        accuracy = accuracy_score(y_test, y_pred)

        # clf save
        model_file_path = os.path.join(output_dir, f"{csv_file.replace('.csv', '.model')}")
        clf.save_model(model_file_path)

        
        result_file_path = os.path.join(evaluation_dir, "result.tsv")
        if not os.path.exists(result_file_path):
            with open(result_file_path, "w") as result_file:
                result_file.write("csv_file\tauc_score\taupr_score\tmcc\tf1_score\taccuracy\n")

        with open(result_file_path, "a") as result_file:
            result_file.write(f"{csv_file}\t{auc_score:.4f}\t{aupr_score:.4f}\t{mcc:.4f}\t{f1:.4f}\t{accuracy:.4f}\n")

        
        roc_plot_path = os.path.join(plot_folder, f"{csv_file.replace('.csv', '_roc.png')}")
        plt.plot(fpr, tpr, label='ROC curve (AUC = {:.2f})'.format(auc_score))
        plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random')
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.legend(loc="lower right")
        plt.savefig(roc_plot_path)
        plt.clf()

        
        all_aucs.append(auc_score)
        all_auprs.append(aupr_score)
        all_mccs.append(mcc)
        all_f1_scores.append(f1)  # Append F1 Score to the list
        all_accuracies.append(accuracy)  # Append Accuracy to the list
        processed_files.add(csv_file)

# average AUC,AUPR,MCC,F1 Score, and Accuracy
mean_auc = sum(all_aucs) / len(all_aucs)
mean_aupr = sum(all_auprs) / len(all_auprs)
mean_mcc = sum(all_mccs) / len(all_mccs)
mean_f1 = sum(all_f1_scores) / len(all_f1_scores)  # Calculate mean F1 Score
mean_accuracy = sum(all_accuracies) / len(all_accuracies)  # Calculate mean Accuracy

with open(result_file_path, "a") as result_file:
    result_file.write("Average\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\n".format(mean_auc, mean_aupr, mean_mcc, mean_f1, mean_accuracy))
