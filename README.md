# hltv_scraper

A module for extracting data from HLTV.org

# Installation

For using this module, just put hltv_scraper.py into directory with your file. Then import module by "import hltv_scraper".

# Functions

## scrape_player_data(driver, weblink, subcat)

A function to grab data for individual players.

Arguments:
- driver : The web driver used to scrape the information. Must be running before the function is called.
- weblink : The actual link that the user wishes to scrape. Must be within hltv.com
- subcat : Accepts 4 unique arguments:
     1. None : Leave this blank to grab the teams and their corresponding players;
     2. flashbangs : Grab the flashbang statistics for each player;
     3. openingkills : Grab the opening kill statistics for each player;
     4. pistols : Grab the pistol round statistics for each player.

## scrape_team_data(driver, weblink, subcat)

A function to grab data for each team for a given date range and subcategory.
    
Arguments:
- driver : The web driver used to scrape the information. Must be running before the function is called.
- weblink : The actual link that the user wishes to scrape. Must be within hltv.com
- subcat : Accepts 3 unique arguments:
  1. None : Overview Category;
  2. ftu : The overall team statistics page;
  3. pistols : The pistol round category.

## scrape_match_data(driver, weblink)
 
A function to scrape different matches between teams for a given time frame.
 
Arguments:
- driver : The web driver used to scrape the information. Must be running before the function is called.
- weblink : The actual link that the user wishes to scrape. Must be within hltv.com
    
Note that unlike the other functions, this one does not take any subcategory arguments.

## scrape(driver, category, date_range, _map, top)
        
A function to scrape different parts of the hltv website.
    
Arguments:
- driver : The web driver used to scrape the information. Must be running before the function is called.
- category : The section of the website that the user chooses to scrape. This may be in the form "category/sub-category". Accepted arguments are:
  1. players/subcat:
      * BLANK : Leave this blank to grab the teams and their corresponding players;
      * flashbangs : Grab the flashbang statistics for each player;
      * openingkills : Grab the opening kill statistics for each player;
      * pistols : Grab the pistol round statistics for each player.
  2. teams/subcat:
      * BLANK : Leave this blank to grab the team overview;
      * ftu : Grab the whole team statistics;
      * pistols : Grab the pistol round information.
  3. matches : Returns all matches for a given map within the specified time frame.
- date_range : How far back in time the data is collected from. Accepted arguments are:
   + 1m : One month;
   + 3m : Three months;
   + 6m : Six months;
   + 12m : Twelve months.
   + YYYY-MM-DD : A specific date
- map : The desired map. Accepted arguments are:
  + all : Grab data for all maps;
  + de_(MAP NAME) : Grab data for any specific map
- top : The desired rankings of teams. Accepted arguments are:
  + 5 : Stats from matches between top 5 teams
  + 10 : Stats from matches between top 10 teams
  + 20 : Stats from matches between top 20 teams
  + 30 : Stats from matches between top 30 teams
  + 50 : Stats from matches between top 50 teams

## scrape_range(driver, category, date_range, _map, top, date_scale)

A function to scrape the running statistics for a given category from the last n days of performance.

Arguments as in the previous function but 1 additional:
- date_scale : an integer number of days for which stats will be collected.

 
 
