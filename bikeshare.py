#!/usr/bin/env python

import time
import pandas as pd
import numpy as np
from collections import Counter


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters(month_list, day_list):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    time.sleep(1)
    
    citydict = {}
    for keys, vals in CITY_DATA.items():
        names = [keys, keys[:3]]
        if " " in keys:
            names.append("".join([splits[0] for splits in keys.split(" ")]))
        citydict[keys] = names
    
    city = ""
    
    while city == "":
        city_input = input("What city/cities would you like to view? \n").lower()
        
        if city_input in CITY_DATA.keys():
            #city_input = ["".join([l for l in list(city_input)])]
            city += city_input
            
        else:
            for i, items in enumerate(citydict.values()):
                if city_input in items:
                    city_input = items[0]
            if city_input in CITY_DATA.keys():
                city += city_input
            else:
                print('Please choose from Chicago, New York City, or Washington.')

    print("You chose:", city)
    time.sleep(0.5)
                
    month = []
    while month == []:
        month_input = input("What month(s) would you like to view? (January to June)\n").lower().replace(" ", "").split(",")

        if "all" in month_input:
            month.append("all")
            
        else:
            for m in month_input:
                try:
                    month.extend([month_list[i] for i in range(len(month_list)) if m in month_list[i]])
                except:
                    print('Please choose from January through June, or "all".')
                    raise
                    
    print("You chose:", month)
    time.sleep(0.5)
    
    day = []
    while day == []:
        day_input = input("Which day(s) of the week would you like to view?\n").lower().replace(" ", "").split(",")
        
        if "all" in day_input:
            day.append("all") 
        
        else:
            for d in day_input:
                try:
                    day.extend([day_list[i] for i in range(len(day_list)) if d in day_list[i]])
                except:
                    print('Please choose from Monday through Sunday, or "all".')
                    raise
        
    print("You chose:", day)
    print('-'*40)
    time.sleep(0.2)
    print("Displaying next section in 5...")
    time.sleep(4)

    return city, month, day


def load_data(city, month, day, month_list, day_list):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df = df.sort_values(by='Trip Duration')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Birth Year'].fillna(method='ffill', axis=0, inplace=True)
    df['Gender'].fillna(method='ffill', axis=0, inplace=True)
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    
    if all(df.isna()) ==  True:
        pass
    else:
        for col in df:
            try:
                all(df[col].isna())
            except:
                print("{} column has {} NaN".format(col, df[col].isna().sum().sum()))
    print("Processing Data...")
    time.sleep(3)
    
    month_dict = {}
    for m in range(len(month_list)):
        month_dict[month_list[m]] = m
    
    if "all" not in month:
        select_month = [month_dict[m] for m in month]
        df = df.loc[df['month'].isin(select_month)]

    day_dict = {}
    for d in range(len(day_list)):
        day_dict[day_list[d]] = d+1
    if "all" not in day:
        select_day = [day_dict[d] for d in day]
        df = df.loc[df['day_of_week'].isin(select_day)]

    return df


def time_stats(df, month_list, day_list):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    time.sleep(1)
    
    start_time = time.time()
    
    df['hour'] = df['Start Time'].dt.hour
    
    print("Most common month: {} ({} out of {})".format(
        month_list[int(df['month'].value_counts().index[0])].upper(),
        int(df['month'].value_counts().max()),
        int(df['month'].value_counts().values.sum())))
    
    print("Most common day of week: {} ({} out of {})".format(
        day_list[int(df['day_of_week'].value_counts().index[0])].upper(),
        int(df['day_of_week'].value_counts().max()),
        int(df['day_of_week'].value_counts().values.sum())))
    
    print("Most popular start hour: {}:00 ({} out of {})".format(
        int(df['hour'].value_counts().index[0]),
        int(df['hour'].value_counts().max()),
        int(df['hour'].value_counts().values.sum())))

    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-'*40)
    time.sleep(0.2)
    print("Displaying next section in 5 seconds...")
    time.sleep(5)
          

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    time.sleep(1)
    
    start_time = time.time()
    
    start_stations = df['Start Station'].value_counts()
    end_stations = df['End Station'].value_counts()
    station_combo = df[['Start Station', 'End Station']].values

    combo_list = []
    for combo in station_combo:
        combo = ' - '.join(combo)
        combo_list.append(combo)
    combo_series = pd.Series(dict(Counter(combo_list))).sort_values(ascending=False)
    
    # TO DO: display most commonly used start station
    print("Top used start station =>  {}  ({} out of {})".format(
        start_stations.index[0],
        int(start_stations.max()),
        int(start_stations.values.sum())))

    # TO DO: display most commonly used end station
    print("Top used end station =>  {}  ({} out of {})".format(
        end_stations.index[0],
        int(end_stations.max()),
        int(end_stations.values.sum())))

    # TO DO: display most frequent combination of start station and end station trip
    print("Top used combination of start/end stations =>  {}  ({} out of {})".format(
        combo_series.index[0],
        int(combo_series.max()),
        int(combo_series.values.sum())))
    
    print("\nThis took %s seconds.\n" % round(time.time() - start_time, 3))
    print('-'*40)
    time.sleep(0.2)
    print("Displaying next section in 5 seconds...")
    time.sleep(5)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    time.sleep(1)
    
    start_time = time.time()

    print("Total travel time: {:.1f}s ({:.1f}hr)".format(
        df['Trip Duration'].sum(),
        df['Trip Duration'].sum()/3600))

    # TO DO: display mean travel time
    print("Average travel time: {:.1f}s ({:.1f}min)".format(
        df['Trip Duration'].sum()/len(df),
        df['Trip Duration'].sum()/len(df)/60))

    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-'*40)
    time.sleep(0.2)
    print("Displaying next section in 5 seconds...")
    time.sleep(5)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    time.sleep(1)
    
    start_time = time.time()
    
    user_count = df['User Type'].value_counts()
    gender_count = df['Gender'].value_counts()
    
    for u in range(len(user_count)):
        print("{} {}s".format(user_count[u], user_count.index[u]))
    print("\n")

    for g in range(len(gender_count)):
        print("{} {}s".format(gender_count[g], gender_count.index[g]))
    print("\n")

    print("Youngest users: age {}".format(
        (int(time.strftime("%Y")) 
         - int(df['Birth Year'].sort_values().max()))
    ))
    print("Oldest users: age {}".format(
        (int(time.strftime("%Y"))
         - int(df['Birth Year'].sort_values().min()))
    ))

    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-'*40)
    time.sleep(0.2)
    print("Data display complete.")


def main():
    month_list = ['all', 'january', 'february', 
                  'march', 'april', 'may', 'june']
    day_list = ['monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday']
    while True:
        city, month, day = get_filters(month_list, day_list)
        df = load_data(city, month, day, month_list, day_list)

        time_stats(df, month_list, day_list)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to view another? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


