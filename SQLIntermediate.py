#counts the rows with data
SELECT COUNT(low) AS low
  FROM tutorial.aapl_historical_stock_price

#see which group in the data set has the most usable data
SELECT COUNT(year) AS year,
       COUNT(month) AS month,
       COUNT(open) AS open,
       COUNT(high) AS high,
       COUNT(low) AS low,
       COUNT(close) AS close,
       COUNT(volume) AS volume
  FROM tutorial.aapl_historical_stock_price

#calculate average price
SELECT SUM(open)/COUNT(open) AS avg_open_price
  FROM tutorial.aapl_historical_stock_price


#calculate lowest value of variable low
SELECT MIN(low)
  FROM tutorial.aapl_historical_stock_price

#calculate highest values of variable low
SELECT MAX(close - open)
  FROM tutorial.aapl_historical_stock_price

#alculate average of a varuable 
SELECT AVG(volume) AS avg_volume
  FROM tutorial.aapl_historical_stock_price

#change in averagte stock price; ordered by group---> order puts it in the order you want --> group groups them without a specific order
SELECT year,
       AVG(close - open) AS avg_daily_change
  FROM tutorial.aapl_historical_stock_price
 GROUP BY 1
 ORDER BY 1

#highest and lowerst price ordered by month 
SELECT year,
       month,
       MIN(low) AS lowest_price,
       MAX(high) AS highest_price
  FROM tutorial.aapl_historical_stock_price
 GROUP BY 1, 2
 ORDER BY 1, 2

#sort players from californa and then order them first 
SELECT player_name,
       state,
       CASE WHEN state = 'CA' THEN 'yes'
            ELSE NULL END AS from_california
  FROM benn.college_football_players
 ORDER BY 3


#group by height and order them as such
SELECT player_name,
       height,
       CASE WHEN height > 76 THEN 'over 76'
            WHEN height > 72 AND height <= 72 THEN '70-72'
            WHEN height > 71 AND height <= 71 THEN '70-71'
            ELSE 'under 70' END AS height_group
  FROM benn.college_football_players

#create a new column with a school year label
SELECT *,
       CASE WHEN year IN ('JR', 'SR') THEN player_name ELSE NULL END AS upperclass_player_name
  FROM benn.college_football_players

#group cases by specific nameing 
SELECT CASE WHEN state IN ('CA', 'OR', 'WA') THEN 'West Coast'
            WHEN state = 'TX' THEN 'Texas'
            ELSE 'Other' END AS arbitrary_regional_designation,
            COUNT(1) AS players
  FROM benn.college_football_players
 WHERE weight >= 300
 GROUP BY 1

#adding the weights of players in a specific group
SELECT CASE WHEN year IN ('FR', 'SO') THEN 'underclass'
            WHEN year IN ('JR', 'SR') THEN 'upperclass'
            ELSE NULL END AS class_group,
       SUM(weight) AS combined_player_weight
  FROM benn.college_football_players
 WHERE state = 'CA'
 GROUP BY 1

#ordering states each having own column 
SELECT state,
       COUNT(CASE WHEN year = 'FR' THEN 1 ELSE NULL END) AS fr_count,
       COUNT(CASE WHEN year = 'SO' THEN 1 ELSE NULL END) AS so_count,
       COUNT(CASE WHEN year = 'JR' THEN 1 ELSE NULL END) AS jr_count,
       COUNT(CASE WHEN year = 'SR' THEN 1 ELSE NULL END) AS sr_count,
       COUNT(1) AS total_players
  FROM benn.college_football_players
 GROUP BY state
 ORDER BY total_players DESC

#order by name of school
SELECT CASE WHEN school_name < 'n' THEN 'A-M'
            WHEN school_name >= 'n' THEN 'N-Z'
            ELSE NULL END AS school_name_group,
       COUNT(1) AS players
  FROM benn.college_football_players
 GROUP BY 1


#shows you all the values in a variable (all unique)
SELECT DISTINCT year
  FROM tutorial.aapl_historical_stock_price
 ORDER BY year

#counts the unique cases in a variable
SELECT year,
       COUNT(DISTINCT month) AS months_count
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year
 ORDER BY year


#create two columns with sorted unique information counts
SELECT COUNT(DISTINCT year) AS years_count,
       COUNT(DISTINCT month) AS months_count
  FROM tutorial.aapl_historical_stock_price


#selects informaiton about a player and then orders them by weight
SELECT players.school_name,
       players.player_name,
       players.position,
       players.weight
  FROM benn.college_football_players players
 WHERE players.state = 'GA'
 ORDER BY players.weight DESC


#joining two tables
SELECT players.player_name,
       players.school_name,
       teams.conference
  FROM benn.college_football_players players
  JOIN benn.college_football_teams teams
    ON teams.school_name = players.school_name
 WHERE teams.division = 'FBS (Division I-A Teams)'

#joins two tables and then sorts them by count of row with non-missing data
SELECT COUNT(companies.permalink) AS companies_rowcount,
       COUNT(acquisitions.company_permalink) AS acquisitions_rowcount
  FROM tutorial.crunchbase_companies companies
  JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink
SELECT COUNT(companies.permalink) AS companies_rowcount,
       COUNT(acquisitions.company_permalink) AS acquisitions_rowcount
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink

#counting two groups from different tables... not includeing missing data
SELECT companies.state_code,
       COUNT(DISTINCT companies.permalink) AS unique_companies,
       COUNT(DISTINCT acquisitions.company_permalink) AS unique_companies_acquired
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink
 WHERE companies.state_code IS NOT NULL
 GROUP BY 1
 ORDER BY 3 DESC

SELECT companies.state_code,
       COUNT(DISTINCT companies.permalink) AS unique_companies,
       COUNT(DISTINCT acquisitions.company_permalink) AS acquired_companies
  FROM tutorial.crunchbase_acquisitions acquisitions
 RIGHT JOIN tutorial.crunchbase_companies companies
    ON companies.permalink = acquisitions.company_permalink
 WHERE companies.state_code IS NOT NULL
 GROUP BY 1
 ORDER BY 3 DESC


#companies in NY --> ordered --> including information about the company
SELECT companies.name AS company_name,
       companies.status,
       COUNT(DISTINCT investments.investor_name) AS unqiue_investors
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments investments
    ON companies.permalink = investments.company_permalink
 WHERE companies.state_code = 'NY'
 GROUP BY 1,2
 ORDER BY 3 DESC

#ordered number of companies with investors... including companies without investors
SELECT CASE WHEN investments.investor_name IS NULL THEN 'No Investors'
            ELSE investments.investor_name END AS investor,
       COUNT(DISTINCT companies.permalink) AS companies_invested_in
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments investments
    ON companies.permalink = investments.company_permalink
 GROUP BY 1
 ORDER BY 2 DESC

#counting the number of rows that join or do not join when connecting two tables
 SELECT COUNT(CASE WHEN companies.permalink IS NOT NULL AND investments.company_permalink IS NULL
                      THEN companies.permalink ELSE NULL END) AS companies_only,
           COUNT(CASE WHEN companies.permalink IS NOT NULL AND investments.company_permalink IS NOT NULL
                      THEN companies.permalink ELSE NULL END) AS both_tables,
           COUNT(CASE WHEN companies.permalink IS NULL AND investments.company_permalink IS NOT NULL
                      THEN investments.company_permalink ELSE NULL END) AS investments_only
      FROM tutorial.crunchbase_companies companies
      FULL JOIN tutorial.crunchbase_investments_part1 investments
        ON companies.permalink = investments.company_permalink

#sorting each dataset by a different variable 
SELECT company_permalink,
       company_name,
       investor_name
  FROM tutorial.crunchbase_investments_part1
 WHERE company_name ILIKE 'T%'
 
 UNION ALL

SELECT company_permalink,
       company_name,
       investor_name
  FROM tutorial.crunchbase_investments_part2
 WHERE company_name ILIKE 'M%'

#not really sure how we got the last more challenging problem. 

