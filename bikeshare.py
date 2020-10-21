import time
import pandas as pd
import numpy as np

#these are the 3 CSV files that we are pulling from to conduct the analysis. PLEASE NOTE THAT THE PATHS WILL NEED TO BE UPDATED.
CITY_DATA = { 'chicago': '/Users/harrison.comfort/python/chicago.csv',
              'new york city': '/Users/harrison.comfort/python/new_york_city.csv',
              'washington': '/Users/harrison.comfort/python/washington.csv'}

#note: since we are pulling data on a monthly and daily basis, I created lists here in the event we want to tweak the months / days that we are analyzing

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday']


#the get_filters() section is important because it is where we paramaterize the data that we will be analyzing

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Please enter chicago, new york city or washington: ")
        if city.lower() in CITY_DATA.keys():
            city = city.lower()
            break

    # get user input for month (all, january, february, ... , june)

    monthly_analysis = input ("Do you want to search by month? Please answer yes or no: ")
    if monthly_analysis == 'no':
        month = 'all'
    else:
        while True:
            month = input("Please the month you'd like to chose from january, february, march, april, may or june in lower case format: ")
            if month.lower() in months:
                month = month.lower()
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    daily_analysis = input ("Do you want to search by day? Please answer yes or no: ")
    if daily_analysis == 'no':
        day = 'all'
    else:
        while True:
            day = input("Please the month you'd like to chose in lower case format. Please answer sunday, monday, tuesday, wednesday, thursday, friday or saturday: ")
            if day.lower() in days:
                day = day.lower()
                break

    print('-'*40)
    return city, month, day

# This load data function, while I don't entirely understand its purpose, *appears* to make it easier to conduct the subsequent analysis
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
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert start time from a string to datetime for purposes of analysis
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #create month and day columns in our dataframe

    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    #if there is a month filter, we need to assign the month to the right integer (i.e. January = 1) for purposes of analysis
    if month != "all":
        month = months.index(month)+1
        df = df[df['month'] == month]

    #filtered by day and we need to capitalize it given the
    if day != "all":
        df = df[df['day']==day.title()]

    return df

#In the spirit of staying organized, we are looking to pull different statistics from the data and the first one is related to time of usage for the bikedata

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    #This is from the template, I assume its purpose is to help understand more efficient ways that code can be written if they take a while

    start_time = time.time()

    # display the most common month, which will trigger an error in searching by month, so I added the while True function here

    while True:
        try:
            common_month = df['month'].mode()[0]
            common_month_name = months[common_month-1]
            print("The most common month for travel is: {}".format(common_month_name))
            break
        except:
            print("The most common month for travel is not relevant since you searched by month!")
            break
    # display the most common day of week, note to change to day_name when back in testing environment. I added a while True function here given it sparks an error if you search by day.

    while True:
        try:
            common_day = (df['day'].mode()[0])
            print("The most common day for travel is: {}".format(common_day))
            break
        except:
            print("The most common day for travel is not relevant since you searched by day!")
            break
    # display the most common start hour. Same logic regarding adding while True. We don't like exceptions.

    while True:
        try:
            df['hour'] = df['Start Time'].dt.hour
            common_hour = df['hour'].mode()[0]
            print("The most common hour for travel is: {}".format(common_hour))
            break
        except:
            print("The most common hour for travel is not relevant since you searched by the day!")
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#displays statistics for the stations

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_ss = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}".format(common_ss))
    # display most commonly used end station

    common_es = df['End Station'].mode()[0]
    print ("The most commonly used end station is: {}".format(common_es))

    # display most frequent combination of start station and end station trip

    df['Start and Finish'] = df['Start Station'] + " 'to' " + df['End Station']
    common_sandf = df['Start and Finish'].mode()[0]
    print("The most frequent combination of start station and end station trip is: {}".format(common_sandf))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#displays statistics for the trip durations

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time... it returns in seconds which is not helpful for anlaysis, so I converted it to hours.


    total_travel_time = df['Trip Duration'].sum()
    print ("The total travel time for this city in this period is: {} hours".format(total_travel_time/360))

    # display mean travel time... it returns in seconds which is not heplful for analysis, so I converted it to minutes.

    mean_travel_time = df['Trip Duration'].mean()
    print ("The average trip duration during this time is: {} minutes".format (mean_travel_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #display stats on users

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender

    while True:
        try:
            gender_counts = df['Gender'].value_counts()
            print(gender_counts)
            break
        except:
            print("There is no gender data for this city!")
            break

    # Display earliest, most recent, and most common year of birth

    while True:
        try:
            recent_birth_year = df['Birth Year'].max()
            print("The most recent birth year is: {}.".format(recent_birth_year))
            break
        except:
            print("There is no birth year data for this city!")
            break

    while True:
        try:
            earliest_birth_year = df['Birth Year'].min()
            print("The most recent birth year is: {}.".format(earliest_birth_year))
            break
        except:
            print("There is no birth year data for this city!")
            break

    while True:
        try:
            common_birth_year = df['Birth Year'].mode()
            common_birth_year = common_birth_year[0]
            print("The most common birth year is: {}.".format(common_birth_year))
            break
        except:
            print("There is no birth year data for this city!")
            break


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    lines = 0
    raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
    while True:
        if raw_data.lower() == 'yes':
            print(df.iloc[lines:lines+5])
            lines+=5
            raw_data = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
