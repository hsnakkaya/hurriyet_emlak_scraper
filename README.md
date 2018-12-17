# hurriyet_emlak_scraper

Scrapes hurriyetemlak.com rental listings and stores in csv files

Pulls and stores; ['Aciklama', 'Konum', 'Tarih', 'Oda', 'Brüt M²', 'Fiyat'] data from page listings.

Use the function; 

emlak_spider(il_var, ilce_var, add_headers) to scrape

-il_var: string list (list of cities to be scraped)

-ilce_var: list of districts to be scraped (optional argument; if used, must use only one item in il_var)

-add_headers: Boolean (optional argument, defaults to True. If you wish to append new data to an existing csv make it False) 
