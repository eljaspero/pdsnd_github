import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("We have data on Chicago, New York City or Washington. Choose a city you want more information on (input should be lowercase): ").lower()
    while city != "chicago" and city != "new your city" and city != "washington":
        print("{} is not a valid city. ".format(city))
        city = input("We have data on Chicago, New York City or Washington. Choose a city you want more information on (input should be lowercase): ").lower()


    month = input("What month would you like information on? Please enter the month in lowercase: ").lower()
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in month_list:
        print("{} is not a valid month. ".format(month))
        month = input("What month would you like information on? Please enter the month in lowercase: ").lower()

    day = input("What day would you like information on? Please enter the day in lowercase: ").lower()
    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in day_list:
        print("{} is not a valid day. ".format(day))
        day = input("What day would you like information on? Please enter the day in lowercase: ").lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('\nThe most common month is {}.\n'.format(popular_month))

    popular_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of week is {}.\n'.format(popular_day))

    df['start_hour'] = df['Start Time'].dt.hour
    popular_hour = df['start_hour'].mode()[0]
    print('\nThe most common start hour is {}.\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most common start station is {}.\n'.format(popular_start_station))

    popular_end_station = df['End Station'].mode()[0]
    print('\nThe most common end station is {}.\n'.format(popular_end_station))

    df['start_stop_combination'] = "Start Station: " + df['Start Station'] + ", End Station: " + df['End Station']
    popular_station_combination = df['start_stop_combination'].mode()[0]
    print('\nThe most common station combination is {}.\n'.format(popular_station_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    tot_trip_duration = df['Trip Duration'].sum()
    print('\nThe total travel time in minutes is {}.\n'.format(tot_trip_duration))

    avg_trip_duration = df['Trip Duration'].mean()
    print('\nThe average travel time in minutes is {}.\n'.format(avg_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('\nCounts of user types:\n')
    print(user_types)

    if city != "washington":
        gender_types = df['Gender'].value_counts()
        print('\nCounts of gender types:\n')
        print(gender_types)


        earliest_birth_year = df['Birth Year'].min()
        print('\nThe earliest birth year is {}.\n'.format(earliest_birth_year))

        most_recent_birth_year = df['Birth Year'].max()
        print('\nThe most recent birth year is {}.\n'.format(most_recent_birth_year))

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nThe most common birth year is {}.\n'.format(most_common_birth_year))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        show_raw_data = input('\nWould you like to see the raw data? Please enter yes or no.\n')
        raw_data_loc = 0
        while show_raw_data.lower() == 'yes':
            print(df.iloc[raw_data_loc:raw_data_loc + 5])
            raw_data_loc += 5
            show_raw_data = input('\nWould you like to see more raw data? Please enter yes or no.\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
