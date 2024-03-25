from flask import Flask, request, jsonify
import pandas as pd
from prophet import Prophet
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def generate_forecast_json(data_file='./sales_mattresstype_format1.csv', forecast_years=2, confidence_interval=0.95):
    # Read the historical data
    historical_data = pd.read_csv(data_file, dayfirst=True)
    # Convert 'Month' column to datetime format
    historical_data['Month'] = pd.to_datetime(historical_data['Month'], dayfirst=True)
    # Rename columns for Prophet model
    historical_data.rename(columns={'Month': 'ds'}, inplace=True)

    # Train Prophet model for each product type
    forecast_df = pd.DataFrame()
    for column in historical_data.columns[1:]:
        model = Prophet(yearly_seasonality=True, seasonality_mode='multiplicative', interval_width=confidence_interval)
        model.add_country_holidays(country_name='SG')
        model.fit(historical_data[['ds', column]].rename(columns={column: 'y'}))
        future = model.make_future_dataframe(periods=forecast_years * 12, freq='M')
        forecast = model.predict(future)
        forecast_df[column] = forecast['yhat'].round()  # Round forecast to nearest integer
        forecast_df[column+'_lower'] = forecast['yhat_lower'].round()
        forecast_df[column+'_upper'] = forecast['yhat_upper'].round()
        forecast_df['ds'] = forecast['ds']

    # Filter forecast dataframe to include data from 2024 onwards
    forecast_years_data = forecast_df.loc[forecast_df['ds'].dt.year >= 2024]

    # Convert historical data to JSON format
    historical_json = []
    for index, row in historical_data.iterrows():
        data = {"Month": row['ds'].strftime('%d/%m/%Y')}
        for column in historical_data.columns[1:]:
            data[column] = int(row[column])  # Convert historical sales to integer
        historical_json.append(data)

    # Convert forecast data to JSON format
    forecast_json = []
    for index, row in forecast_years_data.iterrows():
        data = {"Month": row['ds'].strftime('%d/%m/%Y')}
        for column in historical_data.columns[1:]:
            data[column] = int(row[column])  # Convert forecasted sales to integer
        forecast_json.append(data)

    return historical_json, forecast_json

@app.route('/generate_forecast', methods=['POST'])
def generate_forecast():
    # Generate historical and forecast data
    historical_data, forecast_data = generate_forecast_json()
    
    return jsonify({"historical_data": historical_data, "forecast_data": forecast_data})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
