# The web scraper scripts. This will take a number of key word arguments and return a database with the desired data from the hltv website.

from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date, timedelta
from numpy import random

import pandas as pd
import re
import time

# The below function is responsible for assembling the call link based on our parameters
def build_link(category, date_range, _map, top):

    '''
    Build Link

        A function which takes in the parameters of the web scrape and assembles a link that can be used by the scraper functions.

    Arguments (accepted entries are listed in the "scrape" function docstring):
    
        - category : The category filter;
        - date_range : The date range filter;
        - _map : The maps chosen in the filter.
	- top : The ranking filter.
    '''

    # Properly assemble the date range
    if date_range == '1m':
        date_range = 'startDate=' + str(date.today() - timedelta(days=31)) + '&endDate=' + str(date.today())
    elif date_range == '3m':
        date_range = 'startDate=' + str(date.today() - timedelta(days=92)) + '&endDate=' + str(date.today())
    elif date_range == '6m':
        date_range = 'startDate=' + str(date.today() - timedelta(days=183)) + '&endDate=' + str(date.today())
    elif date_range == '12m':
        date_range = 'startDate=' + str(date.today() - timedelta(days=365)) + '&endDate=' + str(date.today())
    else:
        if type(date_range == list): # If it is a list, grab the contents
            date_range = 'startDate=' + date_range[0] + '&endDate=' + date_range[1]
        else: # If else, assume it is a single date, and grab its contents
            date_range = 'startDate='+ date_range + '&endDate=' + date_range

    if _map == 'all':
        _map = ''
    else:
        _map = '&maps=' + _map
    if top == 'all':
        top = ''
    else:
        top = '&rankingFilter=' + top

    return 'https://www.hltv.org/stats/' + category + '?' + date_range + _map + top

#  First we define a function to scrape player data
def scrape_player_data(driver, weblink, subcat):
    
    '''
    Scrape Player Data

        A function to grab data for individual players.

    Arguments:

        - driver : The web driver used to scrape the information. Must be running before the function is called.
        - weblink : The actual link that the user wishes to scrape. Must be within hltv.com
        - subcat : Accepts 4 unique arguments:
            * None : Leave this blank to grab the teams and their corresponding players;
            * flashbangs : Grab the flashbang statistics for each player;
            * openingkills : Grab the opening kill statistics for each player;
            * pistols : Grab the pistol round statistics for each player.
    '''

    # Set up our engine

    driver.get(weblink)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Since there are four sub-categories in the players data, we need to make sure to perform the correct procedure

    if subcat == None:

        players = []
        team = []
        raiting = []
        kd = []

        # Since one player can be in multiple teams, but one team can have multiple players, we will have no index column in the returned dataframe.

        i = 0
        for a in soup.find('table', attrs={'class' : 'stats-table player-ratings-table'}).find('tbody').findAll('tr'):
            i += 1
            
            # Below is the player name
            players.append(a.find('td', attrs = {'class' : 'playerCol'}).find('a').text)
            
            # Below is the first team
            team.append(str(a.find('td', attrs = {'class' : 'teamCol'}).find('a').find('img')).split('"')[1])
            
            kd.append(a.findAll('td')[5].text)
            
            raiting.append(a.find('td', attrs = {'class' : 'ratingCol'}).text)
            
            # Now we search for any other teams in the column
            ex_team = a.find('td', attrs = {'class' : 'teamCol'}).find('span', attrs = {'class' : 'gtSmartphone-only'}).findAll('a') 
            
            # If the player happens to be in more than one team, we need to append the player for multiple teams
            if len(ex_team) > 0:
                for t in ex_team:
                    players.append(a.find('td', attrs = {'class' : 'playerCol'}).find('a').text)
                    team.append(str(t).split('"')[-2])
                    kd.append(a.findAll('td')[5].text)
                    raiting.append(a.find('td', attrs = {'class' : 'ratingCol'}).text)

        team_players = pd.DataFrame({'Player' : players,
                                    'Team' : team,
									'Raiting' : raiting,
                                    'K/D': kd})

        return team_players
    
    elif subcat == 'flashbangs':

        players = []
        thrown = []
        blinded = []
        opp_flashed = []
        diff = []
        assists = []
        success_rate = []

        for a in soup.find('table', attrs = {'class' : 'stats-table player-ratings-table'}).find('tbody').findAll('tr'):
            
            players.append(a.findAll('td')[0].text)
            thrown.append(a.findAll('td')[2].text)
            blinded.append(a.findAll('td')[3].text)
            opp_flashed.append(a.findAll('td')[4].text)
            diff.append(a.findAll('td')[5].text)
            assists.append(a.findAll('td')[6].text)
            success_rate.append(a.findAll('td')[7].text)

        flashes = pd.DataFrame({'Thrown' : thrown,
                            'Blinded' : blinded,
                            'Opp. Flashes' : opp_flashed,
                            'Flash Diff.' : diff,
                            'Flash Assist Rate' : assists,
                            'Flash Success Rate' : success_rate}, index = players)

        return flashes

    elif subcat == 'openingkills':

        players = []
        kpr = []
        dpr = []
        attempts = []
        successes = []
        ok_rating = []

        for a in soup.find('table', attrs = {'class' : 'stats-table player-ratings-table'}).find('tbody').findAll('tr'):
            players.append(a.findAll('td')[0].text)
            kpr.append(a.findAll('td')[2].text)
            dpr.append(a.findAll('td')[3].text)
            attempts.append(a.findAll('td')[4].text)
            successes.append(a.findAll('td')[5].text)
            ok_rating.append(a.findAll('td')[6].text)
            
        opening = pd.DataFrame({'Opening KPR' : kpr,
                            'Opening DPR' : dpr,
                            'Opening Attempts' : attempts,
                            'Opening Success Rate' : successes,
                            'Opening Kill Rating (2)' : ok_rating}, index = players)

        return opening

    elif subcat == 'pistols':

        players = []
        kd_diff = []
        kd = []
        rating = []

        for a in soup.find('table', attrs = {'class' : 'stats-table player-ratings-table'}).find('tbody').findAll('tr'):
            players.append(a.findAll('td')[0].text)
            kd_diff.append(a.findAll('td')[3].text)
            kd.append(a.findAll('td')[4].text)
            rating.append(a.findAll('td')[5].text)
            
        pistols = pd.DataFrame({'KD Diff.' : kd_diff,
                            'KD' : kd,
                            'Pistol Rating (2)' : rating}, index = players)

        return pistols

    else:

        return -1

# Next we'll move onto a function that will get individual team data
def scrape_team_data(driver, weblink, subcat):

    '''
    Scrape Team Data

        A function to grab data for each team for a given date range and subcategory.

    Arguments:

        - driver : The web driver used to scrape the information. Must be running before the function is called.
        - weblink : The actual link that the user wishes to scrape. Must be within hltv.com
        - subcat : Accepts 3 unique arguments:
            + None : Overview Category;
            + ftu : The overall team statistics page;
            + pistols : The pistol round category.
    '''

    # Set up our engine

    driver.get(weblink)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Since there are three sub-categories in the teams data, we need to make sure we match it with the correct procedure
    
    if subcat == None: # Then we have chosen the overview category

        # Set up our columns

        teams = []
        map_count = []
        kd_diff = []
        kd = []
        rating = []

        # Begin the extraction

        for a in soup.find('table', attrs = {'class' : 'stats-table player-ratings-table'}).find('tbody').findAll('tr'):
            teams.append(a.findAll('td')[0].text)
            map_count.append(a.findAll('td')[1].text)
            kd_diff.append(a.findAll('td')[2].text)
            kd.append(a.findAll('td')[3].text)
            rating.append(a.findAll('td')[4].text)

        # Now add everything to the dataframe

        ratings = pd.DataFrame({'Map Count' : map_count,
                                'K/D Diff.' : kd_diff,
                                'K/D' : kd,
                                'Rating' : rating}, index = teams)
        
        return ratings

    elif subcat == 'ftu': # Then we have chosen the FTU category
        
        # Set up our columns

        teams = []
        roundwin = []
        oduel_wins = []
        multikill = []
        fivefour = []
        fourfive = []
        trades = []
        damage = []
        flashassist = []

        # Begin the extraction

        for a in soup.find('table', attrs = {'class' : 'stats-table player-ratings-table ftu gtSmartphone-only'}).find('tbody').findAll('tr'):
            
            teams.append(a.find('td', attrs = {'class' : 'factor-team'}).text)
            roundwin.append(a.findAll('td')[2].text)
            
            oduel_wins.append(a.findAll('td')[3].text)
            multikill.append(a.findAll('td')[4].text)
            
            fivefour.append(a.findAll('td')[5].text)
            fourfive.append(a.findAll('td')[6].text)
            trades.append(a.findAll('td')[7].text)
            
            damage.append(a.findAll('td')[8].text)
            flashassist.append(a.findAll('td')[9].text)

        # Now add everything to the dataframe

        team_stats = pd.DataFrame({'Round Win Rate' : roundwin,
                          'Opening Duel Wins': oduel_wins,
                          'Multikill Rate' : multikill,
                          'FiveVFour' : fivefour,
                          'FourVFive' : fourfive,
                          'Traded Players' : trades,
                          'Util. Dam.' : damage,
                          'Flash Assist' : flashassist}, index = teams)

        return team_stats

    elif subcat == 'pistols': # Then we have chosen the Pistol Rounds category
        
        # Set up our columns

        teams = []
        won_lost = []
        p_win = []
        r2_conv = []
        r2_break = []

        # Begin the extraction

        for a in soup.find('table', attrs = {'class' : 'stats-table player-ratings-table ftu'}).find('tbody').findAll('tr'):
            teams.append(a.findAll('td')[0].text)
            won_lost.append(a.findAll('td')[2].text)
            p_win.append(a.findAll('td')[3].text)
            r2_conv.append(a.findAll('td')[4].text)
            r2_break.append(a.findAll('td')[5].text)
            
        # Now add everything to the dataframe
        
        results = pd.DataFrame({'Won / Lost' : won_lost,
                            'Pistol Win' : p_win,
                            'Round 2 Conversion' : r2_conv,
                            'Round 2 Break' : r2_break}, index = teams)

        return results

    else:
    
        return -1

# And finally we'll define a function to scrape individual match data
def scrape_match_data(driver, weblink):

    '''
    Scrape Match Data

        A function to scrape different matches between teams for a given time frame.

    Arguments:

        - driver : The web driver used to scrape the information. Must be running before the function is called.
        - weblink : The actual link that the user wishes to scrape. Must be within hltv.com

    Note that unlike the other functions, this one does not take any subcategory arguments.
    '''

    driver.get(weblink)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    dates = []
    team1 = []
    team2 = []
    t_1_country = []
    t_2_country = []
    _map = []
    t_1_score = []
    t_2_score = []
    event = []

    # Since this data is collected by the page, we need to 
    # thrown in an 'offset' variable to go between pages
    # e.g. 1554 - (1554 % 50)

    # First we need to know how many entries there are so that we can calculate the correct offsets
    entries = int(soup.find('span', {'class' : 'pagination-data'}).text.split()[-1])
    offset_count = int((entries - (entries % 50)) / 50)

    # Iterate for each offset
    for i in range(1, offset_count + 1):

        # Set the new webstring every time we turn the page
        new_webstring = ''
        
        # Now set up the web string
        if i > 1:
            new_webstring = weblink + '&offset=' + str(i * 50)
        else:
            new_webstring = weblink

        # Pause time temporarily to prevent blocking
        time.sleep(abs(5 + random.randn()))
        
        # Get the soup
        driver.get(new_webstring)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        for a in soup.find('table', attrs = {'class' : 'stats-table matches-table no-sort'}).find('tbody').findAll('tr'):
            # Grab the date
            dates.append(a.find('td', attrs = {'class' : 'date-col'}).find('a').find('div').text)
            
            # Grab the teams
            team1.append(a.findAll('td', attrs = {'class' : 'team-col'})[0].find('a').text)
            team2.append(a.findAll('td', attrs = {'class' : 'team-col'})[1].find('a').text)
            
            # Grab country
            t_1_country.append(a.findAll('td', attrs = {'class' : 'team-col'})[0].select('img')[0]['alt'])
            t_2_country.append(a.findAll('td', attrs = {'class' : 'team-col'})[1].select('img')[0]['alt'])

            # Grab the map
            _map.append(a.find('td', attrs = {'class' : 'statsDetail'}).find('div', attrs = {'class' : 'dynamic-map-name-full'}).text)
            
            # Grab the scores
            t_1_score.append(re.sub(r'[^\w]', '', a.findAll('td', attrs = {'class' : 'team-col'})[0].find('span').text))
            t_2_score.append(re.sub(r'[^\w]', '', a.findAll('td', attrs = {'class' : 'team-col'})[1].find('span').text))
            
            #Grab the event
            event.append(a.find('td', attrs = {'class' : 'event-col'}).find('a').text)
    
    matches = pd.DataFrame({'Date' : dates,
                        'Team1' : team1,
                        'Team2' : team2,
                        'Team1_country' : t_1_country,
                        'Team2_country' : t_2_country,
                        'Map' : _map,
                        'Team1_Score' : t_1_score,
                        'Team2_Score' : t_2_score,
                        'Event' : event})

    return matches

# Below is the one function to rule them all.
def scrape(driver, category, date_range, _map, top):

    '''
    Scrape

        A function to scrape different parts of the hltv website.

    Arguments:

        - driver : The web driver used to scrape the information. Must be running before the function is called.
        - category : The section of the website that the user chooses to scrape. This may be in the form "category/sub-category". Accepted arguments are:

            + players/...
                * BLANK : Leave this blank to grab the teams and their corresponding players;
                * flashbangs : Grab the flashbang statistics for each player;
                * openingkills : Grab the opening kill statistics for each player;
                * pistols : Grab the pistol round statistics for each player.
            + teams/...
                * BLANK : Leave this blank to grab the team overview;
                * ftu : Grab the whole team statistics;
                * pistols : Grab the pistol round information.
            + matches : Returns all matches for a given map within the specified time frame.

        - date_range : How far back in time the data is collected from. Accepted arguments are:

            + 1m : One month;
            + 3m : Three months;
            + 6m : Six months;
            + 12m : Twelve months.
            + YYYY-MM-DD : A specific date

        - map : The desired map. Accepted arguments are:

            + all : Grab data for all maps;
            + de_(MAP NAME) : Grab data for any specific map.
    '''

    # driver - The driver to be used to make the web calls
    # category - The page of data we wish to extract from
    # date_range - How long ago the data recieved is from (lm, 3m, 6m, 12m)
    # map - The desired map. If set to 'all', will just grab general data

    # First make sure all arguments are in lower case:
    category = category.lower()
    _map = _map.lower()

    # If we passed in a list we don't want to apply the lower case method to it
    if type(date_range) != list:
        date_range = date_range.lower()

    # First, let's assemble our web string:
    weblink = build_link(category, date_range, _map, top)
    
    # Terminate if an error occurred
    if weblink == -1: return -1
    
    # Now decide which function we need to use depending on the category.
    cat = category.split('/')

    if len(cat) == 1:
        # If the category list is missing a subcategory, then append None to the end to make later validation easier
        cat.append(None)

    # Now select which function we should be using

    if cat[0] == 'players':

        return scrape_player_data(driver, weblink, cat[1])

    elif cat[0] == 'teams':
    
        return scrape_team_data(driver, weblink, cat[1])
    
    elif cat[0] == 'matches':
    
        return scrape_match_data(driver, weblink)
    
    else:
    
        return -1

# A function to scrape the running statistics for a given category from the last 30 days of performance
def scrape_range(driver, category, date_range, _map, top, date_scale=30):
    
    # Set up a blank dataframe to host our data
    df = pd.DataFrame()
    
    # First see what date range we're dealing with, and get the number of loops we need to do
    loops = None
    
    if date_range == '1m':
        loops = 31
    elif date_range == '3m':
        loops = 92
    elif date_range == '6m':
        loops = 183
    elif date_range == '12m':
        loops = 365
    else:
        return -1
    
    # Now iterate for each date in our date range
    for loop_date in [date.today() - (x * timedelta(days=1)) for x in range(1, loops)]:
        
        # Get the new dataframe depending on the time range
        new_df = scrape(
            driver, 
            category, 
            [str(loop_date - timedelta(days = date_scale)), str(loop_date)], 
            _map,
            top
        )
        
        # Set a random time delay to prevent bot detection
        time.sleep(abs(3 + 0.5 * random.randn()))
        
        # Format the new dataframe correctly
        new_df['Date'] = new_df.apply(lambda x : str(loop_date), axis = 1)
        new_df.reset_index(inplace = True)
        new_df.set_index('Date', inplace = True)
        
        # Now append the new dataframe
        df = pd.concat([df, new_df], axis = 0)
        
    return df
