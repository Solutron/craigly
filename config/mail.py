'''
Created on Feb 16, 2015

@author: dylan.raithel

Dependencies:

pip install BeautifulSoup4
pip install requests
pip install mailer
pip install jinja2
pip install pkg_resources

'''

# Base Imports
import os
from datetime import datetime

# PyPi imports
from jinja2 import Template
from pkg_resources import resource_stream
import mailer

# This can remain fixed
FROM_ADDRESS = os.environ['CRAIGLY_EMAIL_SMTP_FROM']

SMTP_CONFIG = {
    "host": os.environ['CRAIGLY_EMAIL_SMTP_HOST'],
    "port": os.environ['CRAIGLY_EMAIL_SMTP_PORT'],
    "use_tls": True,
    "usr": os.environ['CRAIGLY_EMAIL_SMTP_USER'],
    "pwd": os.environ['CRAIGLY_EMAIL_SMTP_PASS'],
}

ERROR_ADMIN = os.environ['CRAIGLY_EMAIL_ERROR_TO_ADDRESS']

def render_template(template_text, template_vars):
    new_template = Template(template_text)
    return new_template.render(template_vars)

def craigly_mail(listings):
    """ Renders the data from craigly into an email template """
    # Build the email we'll send
    cur_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    message = mailer.Message()
    message.From = FROM_ADDRESS
    message.Subject = 'Craigly Search Results at {}'.format(cur_date)
    message.To = 'draithel@climate.com'
    message.Cc = 'aesimms85@gmail.com'
    # Load the email template
    template_stream = resource_stream('resources', 'mail.html')
    # create a map for the email template
    template_vars = {
        'datetime': cur_date,
        'message': [listing['link'] for listing in listings]
    }
    message.Html = render_template(template_stream.read(), template_vars)
    sender = mailer.Mailer(**SMTP_CONFIG)
    sender.send(message)

