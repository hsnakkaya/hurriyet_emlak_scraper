# hurriyet_emlak_scraper

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Scrapes hurriyetemlak.com rental listings and stores in csv files

Pulls and stores; ['Aciklama', 'Konum', 'Tarih', 'Oda', 'Brüt M²', 'Fiyat'] data from page listings.

Use the function; 

emlak_spider(il_var, ilce_var) to scrape

-il_var: string list (list of cities to be scraped)

-ilce_var: list of districts to be scraped (optional argument; if used, must use only one il_var)
