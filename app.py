# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    temp_array = list()

    if request.method == 'POST':

        batting_team = request.form['batting-team']
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]


        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]


        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])

        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        # Loading the dataset
        df = pd.read_csv("IPL.csv")

        # Keeping only consistent teams
        consistent_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
                            'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
                            'Delhi Daredevils', 'Sunrisers Hyderabad']
        df = df[(df['batting_team'].isin(consistent_teams)) & (df['bowling_team'].isin(consistent_teams))]

        # Removing the first 5 overs data in every match
        df = df[df['overs']<=10.0]

        # Converting the column 'date' from string into datetime object
        from datetime import datetime
        df['start_date'] = df['start_date'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y'))

        # --- Data Preprocessing ---
        # Converting categorical features using OneHotEncoding method
        encoded_df = pd.get_dummies(data=df, columns=['batting_team', 'bowling_team'])

        # Rearranging the columns
        encoded_df = encoded_df[['start_date', 'batting_team_Chennai Super Kings', 'batting_team_Delhi Daredevils', 'batting_team_Kings XI Punjab',
                      'batting_team_Kolkata Knight Riders', 'batting_team_Mumbai Indians', 'batting_team_Rajasthan Royals',
                      'batting_team_Royal Challengers Bangalore', 'batting_team_Sunrisers Hyderabad',
                      'bowling_team_Chennai Super Kings', 'bowling_team_Delhi Daredevils', 'bowling_team_Kings XI Punjab',
                      'bowling_team_Kolkata Knight Riders', 'bowling_team_Mumbai Indians', 'bowling_team_Rajasthan Royals',
                      'bowling_team_Royal Challengers Bangalore', 'bowling_team_Sunrisers Hyderabad',
                      'overs', 'runs', 'wickets', 'runs_last_5', 'wickets_last_5', 'total']]

        # Splitting the data into train and test set
        X_train = encoded_df.drop(labels='total', axis=1)[encoded_df['start_date'].dt.year <= 2016]
        X_test = encoded_df.drop(labels='total', axis=1)[encoded_df['start_date'].dt.year >= 2017]

        y_train = encoded_df[encoded_df['start_date'].dt.year <= 2016]['total'].values
        y_test = encoded_df[encoded_df['start_date'].dt.year >= 2017]['total'].values

        # Removing the 'date' column
        X_train.drop(labels='start_date', axis=True, inplace=True)
        X_test.drop(labels='start_date', axis=True, inplace=True)

        # --- Model Building ---
        # Linear Regression Model
        from sklearn.linear_model import LinearRegression
        regressor = LinearRegression()
        regressor.fit(X_train,y_train)
        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])

        return render_template('result.html', lower_limit = my_prediction-10, upper_limit = my_prediction+5)


if __name__ == '__main__':
	app.run(debug=True)