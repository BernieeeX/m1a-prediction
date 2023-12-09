import os
import pandas as pd
import joblib 
import xgboost as xgb

# path
model_folder = "/home/share/shenglun/workspace/m1apre/model_xgboost/model"
output_folder = "/home/share/shenglun/workspace/m1apre/HEK_predict0.8"
os.makedirs(output_folder, exist_ok=True)

# for every data_HEK dir，  change Probability to 1/0
data_folder = "/home/share/shenglun/workspace/m1apre/data_HEK"
for csv_file in os.listdir(data_folder):
    if csv_file.endswith(".csv"):
        # make fullpath
        csv_path = os.path.join(data_folder, csv_file)

        # data for group by
        data = pd.read_csv(csv_path)
        original_data = data.iloc[:, :4]

        # feature
        X = data.iloc[:, 6:21].astype(float).values

        # call model has the same name
        model_path = os.path.join(model_folder, csv_file.replace(".csv", ".model"))
        if not os.path.exists(model_path):
            print(f"Model file not found for {csv_file}. Skipping...")
            continue

        clf = xgb.Booster(model_file=model_path)
        y_pred_prob = clf.predict(xgb.DMatrix(X))
        threshold = 0.8
        y_pred = [1 if prob >= threshold else 0 for prob in y_pred_prob]
        predictions = y_pred
        
        output_path = os.path.join(output_folder, csv_file)

        # with first 6 arrange
        result_data = pd.concat([original_data, pd.Series(predictions, name='Prediction')], axis=1)
        result_data.to_csv(output_path, index=False)
