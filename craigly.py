'''
Created on Feb 15, 2015

@author: dylan.raithel

Dependencies:

pip install BeautifulSoup4
pip install requests
pip install mailer
pip install jinja2
pip install mechanize


'''

# Base Imports
import sys
import os
from datetime import datetime, timedelta

# PyPi imports
from bs4 import BeautifulSoup
import requests

# Module imports
from config.map_listings import map_listing
from config.mail import craigly_mail


def fetch_search_results(query=None, minAsk=None, maxAsk=None, bedrooms=None):
    """ Passes a dict to requests get for craigslist and returns data """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No Valid Keywords")
    base = 'https://sfbay.craigslist.org/search/eby/apa'
    resp = requests.post(base, params=search_params, timeout=3, headers=headers)
    resp.raise_for_status() # <- no-op if status==200
    return resp.content, resp.encoding


def parse_source(html, encoding='utf-8'):
    """ Returns a BeautifulSoup class of the html given 
    the encoding """
    parsed = BeautifulSoup(html)
    return parsed


def write_search_results(content, encoding):
    """ Takes as input the content and encoding
    returned from get_results and returns a filename
    for use in the resource stream """
    today_string = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    filename = "{}.html".format(today_string)
    writepath = os.path.join('resources', filename)
    with open(writepath, 'w') as f:
        f.write(content)
        f.close()
    return filename


def remove_search_results(filename):
    delete_path = os.path.join('resources', filename)
    os.remove(delete_path)


def read_search_results(filename):
    """ Takes as input the filename and encoding of the file 
    and returns a readable doc object """
    readfile = os.path.join('resources', filename)
    with open(readfile, 'r') as f:
        html = f.read()
    return html


def extract_listings(parsed):
    """ Plucks out some useful info from the Soupy html tree """
    # stub for plucking attributes
    time_attrs = {'time datetime': True, 'title': True}
    listings = parsed.find_all('p', class_='row')
    extracted = []
    raw_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    cur_date = datetime.strptime(raw_date, '%Y-%m-%d %H:%M')
    for listing in listings:
        this_listing = map_listing(listing)
        posted_at = datetime.strptime(this_listing['wallclock'], '%Y-%m-%d %H:%M') 
        time_limit = posted_at + timedelta(minutes=60)
        if time_limit > cur_date:
            extracted.append(this_listing)
    return extracted


if __name__ == '__main__':
    
    """ Teh robotz take over house hunt...
    """

    # Call Craigslist and get all the postng things
    html, encoding = fetch_search_results( minAsk=1500, 
        maxAsk=1850, bedrooms=1
    )

    # Write those postings to file
    filename = write_search_results(html, encoding)

    # Read from that file and don't irritate Craigslist
    # by calling them more than once... every five minutes
    html = read_search_results(filename)

    # parse the html and print it
    parsed = parse_source(html)
    print parsed.prettify(encoding=encoding)

    # Get some listings
    listings = extract_listings(parsed)

    # send yo email
    craigly_mail(listings)

    # delete the temp file
    remove_search_results(filename)
