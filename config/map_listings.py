'''
Created on Feb 16, 2015

@author: dylan.raithel

Dependencies:

pip install BeautifulSoup4
pip install requests
pip install mailer
pip install jinja2

'''

def map_listing(listing):
    """ Map the tree nodes we care about to a dict """
    # These are raw data
    link = listing.find('span', class_='pl').find('a')
    # mapped
    this_listing = {
            'location': listing.find('span', class_='pnr').find('small').string.split(),
            'price': listing.find('span', class_='l2').find('span', class_='price'),
            'wallclock': str(listing.find('span', class_='pl').find('time').attrs['datetime']),
            'calendar': listing.find('span', class_='pl').find('time').attrs['title'],
            'description': link.string.strip(),
            'housing': listing.find('span', class_='housing'),
            'link': 'https://sfbay.craigslist.org'+link.attrs['href']  
        }
    return this_listing