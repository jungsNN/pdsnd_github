# !/usr/bin/env python
import time
import pandas as pd
import numpy as np
from collections import Counter


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def print_pause(string, n):
    """Delays next display for n seconds using time.sleep() function.

    Parameters
    ----------
    string (str):
        string value to print out

    n (int):
        number of seconds to pass into sleep.time() function
    """
    print(string)
    time.sleep(g)


def get_filters(month_list, day_list):
    """
    Asks user to specify a city, month, and day to analyze.

    Parameters
    ----------
    month_list (list):
        list of string values from 'january' to 'june';
        "all" is the first item in the list;
        months' indices match the Pandas datetime month values
    day_list (list):
        list of strings values from 'monday' to 'sunday';
        indexing matches that of Pandas' datetime weekday values

    Returns
    -------
    city (str):
        name of the city to analyze
    month (list):
        name of the month to filter by, or
        "all" to apply no month filter
    day (list):
        name of the day of week to filter by, or
        "all" to apply no day filter
    """
    print_pause('Hello! Let\'s explore some US bikeshare data!', 1)

    citydict = {}
    for keys, vals in CITY_DATA.items():
        names = [keys, keys[:3]]
        if " " in keys:
            names.append("".join([splits[0] for splits in keys.split(" ")]))
        citydict[keys] = names

    city = ""
    while city == "":
        city_input = (input("What city/cities would you like to view? \n")
                      .lower())
        if city_input in CITY_DATA.keys():
            city += city_input
        else:
            for i, items in enumerate(citydict.values()):
                if city_input in items:
                    city_input = items[0]
            if city_input in CITY_DATA.keys():
                city += city_input
            else:
                print('Please choose from \
                      Chicago, \
                      New York City, \
                      or Washington.')

    print_pause("You chose: ".format(city), 0.3)

    month = []
    while month == []:
        month_input = (
            input("What month(s) would you like to view? [January-June]\n")
            .lower()
            .replace(" ", "")
            .split(",")
            )
        if "all" in month_input:
            month.append("all")
        else:
            for m in month_input:
                try:
                    month.extend([month_list[i]
                                  for i in range(len(month_list))
                                  if m in month_list[i]])
                except Exceptions as e:
                    print('Please choose from January through June, or "all".')
                    pass

    print_pause(("You chose:", month), 0.3)

    day = []
    while day == []:
        day_input = (
            input("Which day(s) of the week would you like to view?\n")
            .lower()
            .replace(" ", "")
            .split(",")
            )
        if "all" in day_input:
            day.append("all")
        else:
            for d in day_input:
                try:
                    day.extend([day_list[i]
                                for i in range(len(day_list))
                                if d in day_list[i]])
                except Exception as e:
                    print('Please choose from \
                          Monday through Sunday, \
                          or "all".')
                    pass

    print_pause(("You chose:", day), 0.3)

    print('-'*40)
    print_pause("Displaying next section in 5...", 4)

    return city, month, day


def load_data(city, month, day, month_list, day_list):
    """Loads data for the specified city and filters by month and day
    if applicable.

    Parameters
    ----------
    city (str):
        name of the city to analyze
    month (list):
        name of the month to filter by, or "all" to apply no
        month filter
    day (list):
        name of the day of week to filter by, or
        "all" to apply no day filter

    Returns
    -------
    df (Pandas DataFrame):
        dataset containing city data filtered by
        month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df = df.sort_values(by='Trip Duration')

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if 'Gender' in df.columns:
        df['Birth Year'].fillna(method='ffill', axis=0, inplace=True)
        df['Gender'].fillna(method='ffill', axis=0, inplace=True)

    if all(df.isna()):
        continue
    else:
        for col in df:
            if df[col].isna().sum().sum() != 0:
                try:
                    df[col].fillna(method='ffill', axis=0, inplace=True)
                    df[col].isna().sum().sum() == 0
                except Exception as e:
                    print("{} column has {} NaN"
                          .format(col, df[col].isna().sum().sum()))
                    pass

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


def display_data(df):
    """Displays raw dataset 5 rows at a time upon user's request."""

    show_ask = input("Would you like to view the raw data? \n\
        (press enter to view 5 rows at a time, 'q' to pass)\n")

    if show_ask == "\\n":
        row_counter = 0

        while len(df) >= 0:
            if row_counter > (len(df)-5):
                print(df[row_counter:])
                break

            print(df[row_counter:row_counter+5])

            show_ask = input("Enter key to view next 5 rows/'q' to end: ")

            if show_ask == "\\n":
                row_counter += 5
                len(df) -= 5
            elif show_ask == "q":
                len(df) = -1
                break


def time_stats(df, month_list, day_list):
    """Displays statistics on the most frequent times of travel.

    Parameters
    ----------
    df (Pandas DataFrame):
        filtered dataset to evaluate
    """

    print_pause('\nCalculating The Most Frequent Times of Travel...\n', 1)

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

    print_pause(("\nThis took %s seconds." %
                 round(time.time() - start_time, 3)), 0.2)

    print('-'*40)
    print_pause("Displaying next section in 5 seconds...", 5)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print_pause('\nCalculating The Most Popular Stations and Trip...\n', 1)

    start_time = time.time()

    start_stations = df['Start Station'].value_counts()
    end_stations = df['End Station'].value_counts()
    station_combo = df[['Start Station', 'End Station']].values

    combo_list = []
    for combo in station_combo:
        combo = ' - '.join(combo)
        combo_list.append(combo)

    combo_series = pd.Series(dict(Counter(combo_list))
                             .sort_values(ascending=False))

    print("Top used start station: {} ({} out of {})"
          .format(start_stations.index[0],
                  int(start_stations.max()),
                  int(start_stations.values.sum())))
    print("Top used end station: {} ({} out of {})"
          .format(end_stations.index[0],
                  int(end_stations.max()),
                  int(end_stations.values.sum())))
    print("Top used combination of start/end stations: {} ({} out of {})"
          .format(combo_series.index[0],
                  int(combo_series.max()),
                  int(combo_series.values.sum())))

    print_pause(("\nThis took %s seconds.\n" %
                 round(time.time() - start_time, 3)), 0.3)

    print('-'*40)
    print_pause("Displaying next section in 5 seconds...", 5)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print_pause('\nCalculating Trip Duration...\n', 1)

    start_time = time.time()

    print("Total travel time: {:.1f}s ({:.1f}hr)"
          .format(df['Trip Duration'].sum(),
                  df['Trip Duration'].sum()/3600))
    print("Average travel time: {:.1f}s ({:.1f}min)"
          .format(df['Trip Duration'].sum()/len(df),
                  df['Trip Duration'].sum()/len(df)/60))

    print_pause(("\nThis took %s seconds." %
                 round(time.time() - start_time, 3)), 0.2)

    print('-'*40)
    print_pause("Displaying next section in 5 seconds...", 5)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print_pause('\nCalculating User Stats...\n', 1)
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
         - int(df['Birth Year'].sort_values().max()))))
    print("Oldest users: age {}"
          .format((int(time.strftime("%Y"))-int(df['Birth Year']
                                                .sort_values().min()))))

    print_pause(("\nThis took %s seconds." %
                 round(time.time() - start_time, 3)), 0.3)

    print('-'*40)
    print_pause("Data display complete.", 1)


def main():
    month_list = ['all', 'january', 'february',
                  'march', 'april', 'may', 'june']
    day_list = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']

    while True:
        city, month, day = get_filters(month_list, day_list)
        df = load_data(city, month, day, month_list, day_list)

        time_stats(df, month_list, day_list)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to view another? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
