import pandas as pd
import pickle


def encode_one (data, column_name = 'Airline'):
    column = data[column_name]
    column = pd.get_dummies(column, drop_first=True)
    data.drop (column_name, axis = 1, inplace=True)
    data = pd.concat ([data, column], axis = 1)
    return data


def extract_date (data, column, format = None):
    if format is not None:
        data[f"{column}_day"] = pd.to_datetime(data[column], format=format).dt.day
        data[f"{column}_month"] = pd.to_datetime(data[column], format=format).dt.month
        data.drop (column, inplace=True, axis = 1)
    else:
        data[f"{column}_hour"] = pd.to_datetime(data[column]).dt.hour
        data[f"{column}_min"] = pd.to_datetime(data[column]).dt.minute
        data.drop (column, inplace=True, axis = 1)

    return data


def get_hour_min (hour_array, min_array, string):
    string = string.split (' ')
    if len(string) == 1:
        string.append ('0m')

    hour_array.append(int(string[0][:-1]))
    min_array.append(int(string[1][:-1]))

    return hour_array, min_array


def handle_duration (data):
    duration = list (data.Duration)
    duration_hour = []
    duration_min = []
    for i in range (len(duration)):
        duration_hour, duration_min = get_hour_min(duration_hour, duration_min, duration[i])

    data['Duration_hour'] = duration_hour
    data['Duration_min'] = duration_min
    data.drop ('Duration', axis = 1, inplace=True)
    return data


def extract_data (file_path = 'data/train_data.csv'):
    data = pd.read_csv (file_path)
    data.dropna(inplace=True)
    data.drop (['Additional_Info', 'Route'], inplace = True, axis = 1)
    data = encode_one(data, column_name='Airline')
    data = encode_one(data, column_name='Source')
    data = encode_one(data, column_name='Destination')
    data.replace ({'non-stop': 0,
                    '1 stop': 1,
                    '2 stops': 2,
                    '3 stops': 3,
                    '4 stops':4},
                  inplace = True
                  )
    data = extract_date(data, 'Date_of_Journey', format = '%d/%m/%Y')
    data = extract_date(data, 'Dep_Time')
    data = extract_date(data, 'Arrival_Time')
    data = handle_duration (data)

    return data


def get_train_data():
    train = extract_data()
    y = train['Price']
    X = train.drop ('Price', axis = 1)
    with open ('train_clean_data.pkl', 'wb') as file:
        pickle.dump((X, y), file)


def get_test_data():
    test = extract_data()
    with open('test_data.pkl', 'wb') as file:
        pickle.dump(test, file)


if __name__ == "__main__":
    get_train_data()
    # get_test_data()