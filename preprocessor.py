import pandas as pd
import re

def preprocess(data):
    # Pattern to extract messages and timestamps
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[\u202f]?[APap][Mm]\s-\s'
    messages = re.split(pattern, data)[1:]  # Skip the first empty split
    dates = re.findall(pattern, data)

    # Replace special character '\u202f' in dates
    dates = [date.replace('\u202f', ' ') for date in dates]

    # Ensure messages and dates have the same length
    if len(messages) != len(dates):
        raise ValueError("Mismatch between number of messages and dates.")

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    clean_messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:  # If a user is identified
            users.append(entry[1])
            clean_messages.append(entry[2])
        else:  # System notifications or messages without a user
            users.append('group_notification')
            clean_messages.append(entry[0])

    # Add users and cleaned messages to the DataFrame
    df['users'] = users
    df['message'] = clean_messages
    df.drop(columns=['user_message'], inplace=True)

    # Add additional date-related columns
    df['only_date']=df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour == 2:
            period.append(str(hour)+"-"+str('00'))
        elif hour == 0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period
    return df
