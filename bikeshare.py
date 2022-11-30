import time
import pandas as pd
import numpy as np

# Allows user to view all columns if they choose to view raw data--from Udacity project reviewer code comments
pd.set_option(“display.max_columns”,200)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
days = ['monday', 'tuesday', 'wedesnday', 'thursday', 'friday', 'saturday', 'sunday']
months = ['january','february','march','april','may','june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to explore data for Chicago, New York City, or Washington?').lower()
            filename = CITY_DATA[city]
            break
        except:
            print('Please enter a valid city. Chicago, New York City, or Washington?')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            # get month from user input
            month = input('Which month would you like to look at? January, February, March, April, May, June, or All?').lower()
            
            # filter for month or no filter if 'all'
            if month != 'all':
                
                # get int for corresponding month
                # months = ['january','february','march','april','may','june']
                month_index = months.index(month) + 1
            break
        except:
            print('Please enter a valid month. January, February, March, April, May, June, or All?')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Which day would you like to look at? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?').lower()
            if day != 'all':
                # days = ['monday', 'tuesday', 'wedesnday', 'thursday', 'friday', 'saturday', 'sunday']
                day_index = days.index(day)
            break
        except:
            print('Please enter a valid day. Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All?')

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
    df = pd.read_csv(CITY_DATA[city])
            
    # create month column from the start time column
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    
    # filter for month or no filter if 'all'
    if month.lower() != 'all':
        # get int for corresponding month
        # months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        
        # filter by month given
        df = df[df['month'] == month]
    
    # create day column
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    
    # filter by day given
    if day != 'all':
        # days = ['monday', 'tuesday', 'wedesnday', 'thursday', 'friday', 'saturday', 'sunday']
        day_index = days.index(day)
        df = df[df['day_of_week'] == day_index]
        
    # create start hour column
    df['start_hour'] = df['Start Time'].dt.hour
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_pop = df['month'].mode()[0]
    print('The most popular month is {}.'.format(months[month_pop - 1].title()))

    # TO DO: display the most common day of week
    day_pop = df['day_of_week'].mode()[0]
    print('The most popular weekday is {}.'.format(days[day_pop].title()))

    # TO DO: display the most common start hour
    hour_pop = df['start_hour'].mode()[0]
    print('The most popular hour to start is {}:00.'.format(hour_pop))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most popular station to start from is {}.'.format(start_station))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most popular station to end at is {}.'.format(end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['start-stop'] = df['Start Station'] + ' and ' + df['End Station']
    station_combo = df['start-stop'].mode()[0]
    print('The most popular start and end station combination is {}.'.format(station_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_time = df['Trip Duration'].sum()
    tot_time_hr= int(tot_time / 3600)
    tot_time_min = int((tot_time - tot_time_hr * 3600)/ 60)
    tot_time_sec = tot_time - tot_time_hr * 3600 - tot_time_min * 60
    print('The total travel time is {} hours, {} minutes, and {} seconds.'.format(tot_time_hr, tot_time_min, tot_time_sec))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time_hr= int(mean_time / 3600)
    mean_time_min = int((mean_time - mean_time_hr * 3600)/ 60)
    mean_time_sec = mean_time - mean_time_hr * 3600 - mean_time_min * 60
    print('The total travel time is {} hours, {} minutes, and {:.2F} seconds.'.format(mean_time_hr, mean_time_min, mean_time_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print('Counts of User Types')
    print(user_types)

    # TO DO: Display counts of gender
    # While True:
    try:
        gender = df.groupby(['Gender'])['Gender'].count()
    except:
        print('There is no gender data for users in this city.')
    else:
        print('Counts of Genders')
        print(gender)        

    # TO DO: Display earliest, most recent, and most common year of birth
    
    try:
        early_yr = int(df['Birth Year'].min())
    except:
        print('There is no birth year data for users in this city.')
    else:
        late_yr = int(df['Birth Year'].max())
        common_yr = int(df['Birth Year'].mode()[0])
        print('The earliest user birth year is {}.'.format(early_yr))
        print('The most recent user bith year is {}.'.format(late_yr))
        print('The most common user birth year is {}.'.format(common_yr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Ask user if they want to view raw data
        count = 5
        while True:
            if count == 5:
                data = input('\nWould you like to view five rows of the raw data? Enter yes or no.\n')
            else:
                data = input('\nWould you like to view five more rows of the raw data? Enter yes or no.\n')
            # if yes, show 5 rows, then prompt again
            if data.lower() == 'yes':
                print(df.iloc[(count - 5) : count])
                count += 5
                continue
            
            # if no, go to restart option
            elif data.lower() == 'no':
                break
            
            # if input is neither yes nor no, ask again
            else:
                continue

        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
