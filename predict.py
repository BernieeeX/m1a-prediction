import os
import pandas as pd
import joblib 
import xgboost as xgb
import argparse

def predict_with_xgboost(input_folder, output_folder, model_folder):
    os.makedirs(output_folder, exist_ok=True)

    for csv_file in os.listdir(input_folder):
        if csv_file.endswith(".csv"):
            # make full path
            csv_path = os.path.join(input_folder, csv_file)

            # data for group by
            data = pd.read_csv(csv_path)
            original_data = data.iloc[:, :4]

            # feature
            X = data.iloc[:, 7:22].astype(float).values

            # call model has the same name
            model_path = os.path.join(model_folder, csv_file.replace(".csv", ".model"))
            if not os.path.exists(model_path):
                print(f"Model file not found for {csv_file}. Skipping...")
                continue

            clf = xgb.Booster(model_file=model_path)
            y_pred_prob = clf.predict(xgb.DMatrix(X))
            threshold = 0.5
            y_pred = [1 if prob >= threshold else 0 for prob in y_pred_prob]
            predictions = y_pred

            output_path = os.path.join(output_folder, csv_file)

            # with first 6 arrange
            result_data = pd.concat([original_data, pd.Series(predictions, name='Prediction')], axis=1)
            result_data.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make predictions with XGBoost model.")
    parser.add_argument("-i", "--input", help="Input folder containing CSV files", required=True)
    parser.add_argument("-o", "--output", help="Output folder for predictions", required=True)
    parser.add_argument("-m", "--models", help="Folder containing XGBoost models", required=True)
    args = parser.parse_args()

    predict_with_xgboost(args.input, args.output, args.models)
