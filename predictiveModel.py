import pandas as pd
import sqlFunction as sql
import mysql
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score


def load_and_prepare_data():
    
    sqlString="SELECT `2023_2024_events`.`elements`.*,`2023_2024_bootstrapstatic`.`elements`.`element_type`,`2023_2024_bootstrapstatic`.`elements`.`ep_next`,`2023_2024_bootstrapstatic`.`elements`.`ep_this`,`2023_2024_bootstrapstatic`.`elements`.`event_points`,`2023_2024_bootstrapstatic`.`elements`.`first_name`,`2023_2024_bootstrapstatic`.`elements`.`form`,`2023_2024_bootstrapstatic`.`elements`.`news`,`2023_2024_bootstrapstatic`.`elements`.`news_added`,`2023_2024_bootstrapstatic`.`elements`.`now_cost`,`2023_2024_bootstrapstatic`.`elements`.`photo`,`2023_2024_bootstrapstatic`.`elements`.`points_per_game`,`2023_2024_bootstrapstatic`.`elements`.`second_name`,`2023_2024_bootstrapstatic`.`elements`.`selected_by_percent`,`2023_2024_bootstrapstatic`.`elements`.`special`,`2023_2024_bootstrapstatic`.`elements`.`squad_number`,`2023_2024_bootstrapstatic`.`elements`.`status`,`2023_2024_bootstrapstatic`.`elements`.`team`,`2023_2024_bootstrapstatic`.`elements`.`team_code`,`2023_2024_bootstrapstatic`.`elements`.`transfers_in`,`2023_2024_bootstrapstatic`.`elements`.`transfers_in_event`,`2023_2024_bootstrapstatic`.`elements`.`transfers_out`,`2023_2024_bootstrapstatic`.`elements`.`transfers_out_event`,`2023_2024_bootstrapstatic`.`elements`.`value_form`,`2023_2024_bootstrapstatic`.`elements`.`value_season`,`2023_2024_bootstrapstatic`.`elements`.`web_name`,`2023_2024_bootstrapstatic`.`elements`.`influence_rank`,`2023_2024_bootstrapstatic`.`elements`.`influence_rank_type`,`2023_2024_bootstrapstatic`.`elements`.`creativity_rank`,`2023_2024_bootstrapstatic`.`elements`.`creativity_rank_type`,`2023_2024_bootstrapstatic`.`elements`.`threat_rank`,`2023_2024_bootstrapstatic`.`elements`.`threat_rank_type`,`2023_2024_bootstrapstatic`.`elements`.`ict_index_rank`,`2023_2024_bootstrapstatic`.`elements`.`ict_index_rank_type`,`2023_2024_bootstrapstatic`.`elements`.`corners_and_indirect_freekicks_order`,`2023_2024_bootstrapstatic`.`elements`.`corners_and_indirect_freekicks_text`,`2023_2024_bootstrapstatic`.`elements`.`direct_freekicks_order`,`2023_2024_bootstrapstatic`.`elements`.`direct_freekicks_text`,`2023_2024_bootstrapstatic`.`elements`.`penalties_order`,`2023_2024_bootstrapstatic`.`elements`.`penalties_text`,`2023_2024_bootstrapstatic`.`elements`.`expected_goals_per_90`,`2023_2024_bootstrapstatic`.`elements`.`saves_per_90`,`2023_2024_bootstrapstatic`.`elements`.`expected_assists_per_90`,`2023_2024_bootstrapstatic`.`elements`.`expected_goal_involvements_per_90`,`2023_2024_bootstrapstatic`.`elements`.`expected_goals_conceded_per_90`,`2023_2024_bootstrapstatic`.`elements`.`goals_conceded_per_90`,`2023_2024_bootstrapstatic`.`elements`.`now_cost_rank`,`2023_2024_bootstrapstatic`.`elements`.`now_cost_rank_type`,`2023_2024_bootstrapstatic`.`elements`.`form_rank`,`2023_2024_bootstrapstatic`.`elements`.`form_rank_type`,`2023_2024_bootstrapstatic`.`elements`.`points_per_game_rank`,`2023_2024_bootstrapstatic`.`elements`.`points_per_game_rank_type`,`2023_2024_bootstrapstatic`.`elements`.`selected_rank`,`2023_2024_bootstrapstatic`.`elements`.`selected_rank_type`,`2023_2024_bootstrapstatic`.`elements`.`starts_per_90`,`2023_2024_bootstrapstatic`.`elements`.`clean_sheets_per_90` FROM `2023_2024_events`.`elements` INNER JOIN `2023_2024_bootstrapstatic`.`elements` ON `2023_2024_events`.`elements`.`id` = `2023_2024_bootstrapstatic`.`elements`.`id`;"

    mydb = mysql.connector.connect(
        host="localhost",
        user='jackbegley',
        password='Athome19369*',
        database='2023_2024_events'
    )

    result = dict()
    mycursor = mydb.cursor()
    mycursor.execute(sqlString)
    columnNames = mycursor.column_names
    myresult = mycursor.fetchall()
    columns = {}

    for name in columnNames:
        columns[name] = []

    for row in myresult:
        for idx, value in enumerate(row):
            columnName = columnNames[idx]
            columns[columnName].append(value)
    
    df = pd.DataFrame(columns)

    return df

def create_features(data):
    # Create the binary target variable and features
    # Replace the column names with the actual column names from your data
    data['Outperformed_EP'] = (data['event_points'] > data['ep_this'])
    data['Outperformed_EP'] = data['Outperformed_EP'].apply(lambda x: 1 if x else 0)
    features = data[['gameweek','id','minutes','goals_scored','assists','clean_sheets','goals_conceded','own_goals','penalties_saved','penalties_missed','yellow_cards','red_cards','saves','bonus','bps','influence','creativity','threat','ict_index','starts','expected_goals','expected_assists','expected_goal_involvements','expected_goals_conceded','total_points','in_dreamteam','fixture','minutes_points','minutes_value','assists_points','assists_value','goals_scored_points','goals_scored_value','bonus_points','bonus_value','goals_conceded_points','goals_conceded_value','saves_points','saves_value','yellow_cards_points','yellow_cards_value','clean_sheets_points','clean_sheets_value','red_cards_points','red_cards_value','element_type','ep_next','form','now_cost','points_per_game','selected_by_percent','special','squad_number','team','team_code','transfers_in','transfers_in_event','transfers_out','transfers_out_event','value_form','value_season','influence_rank','influence_rank_type','creativity_rank','creativity_rank_type','threat_rank','threat_rank_type','ict_index_rank','ict_index_rank_type','corners_and_indirect_freekicks_order','direct_freekicks_order','penalties_order','expected_goals_per_90','saves_per_90','expected_assists_per_90','expected_goal_involvements_per_90','expected_goals_conceded_per_90','goals_conceded_per_90','now_cost_rank','now_cost_rank_type','form_rank','form_rank_type','points_per_game_rank','points_per_game_rank_type','selected_rank','selected_rank_type','starts_per_90','clean_sheets_per_90']] 
    target = data['Outperformed_EP']
    return features, target

def train_model(X, y, n_estimators=100, learning_rate=0.1, max_depth=3):
    # Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training with manual parameter tuning
    model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)

    # Model evaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy}")

    return model

def make_prediction(model, input_data):
    # Predicting with the model
    prediction = model.predict([input_data])
    return prediction

if __name__ == "__main__":
    # Load and prepare data
    data = load_and_prepare_data()

    # Create features and target
    X, y = create_features(data)

    # Train the model with manual parameter tuning
    # Adjust these parameters as needed
    n_estimators = 350
    learning_rate = 0.01
    max_depth = 6
    model = train_model(X, y, n_estimators, learning_rate, max_depth)

    # Example prediction
    # Replace 'input_data' with actual data for prediction
    test_data = [11, 5, 90, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 12, 19.0, 2.0, 2.0, 2.3, 1, 0.00, 0.03, 0.03, 1.09, 2, 0, 2, 2, 90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1.8, 1.3, 48, 2.9, 15.2, 0, 0, 1, 3, 907107, 71642, 2295499, 39345, 0.3, 6, 164, 65, 304, 102, 208, 52, 234, 73, 0, 0, 0, 0, 0, 0, 0, 1, 1, 302, 35, 223, 76, 145, 49, 22, 7, 1, 0]  # Example input, replace with actual data
    prediction = make_prediction(model, test_data)
    print(f"Prediction: {prediction}")
    print("")
