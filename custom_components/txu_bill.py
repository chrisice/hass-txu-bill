import mechanicalsoup
from bs4 import BeautifulSoup
import re

DOMAIN = 'txu_bill'

def setup(hass, config):
    browser = mechanicalsoup.Browser(
        soup_config={'features': 'lxml'},
    )

    page_url = "https://www.txu.com/myaccount/residential/bill-payments/view-bill.aspx"
    username = config['txu_bill']['username']
    password = config['txu_bill']['password']
    login_page = browser.get(page_url)
    login_form = mechanicalsoup.Form(
    login_page.soup.select_one('form[method="post"]'))
    login_form.input({'ctl00$ContentPlaceHolderMain$ctl01$ctl00$txuLoginModule$txtUsername': username, 'ctl00$ContentPlaceHolderMain$ctl01$ctl00$txuLoginModule$txtPassword': password})

    response = browser.submit(login_form, page_url)
    textout = response.soup.find_all("div", class_="view-bill-left")

    for texts in textout:
        line = re.sub('\s+', ' ', texts.text)
        billed = re.search('(?<=Total Billed Amount ).+?[0-9]\s', line)
        hours = re.search('(?<=Total kWh Used ).+?[0-9]\s', line)
        due = re.search('(?<=Due Date ).+', line)

    hass.states.set('txu_bill.txu_billed', billed[0])
    hass.states.set('txu_bill.txu_hours', hours[0])
    hass.states.set('txu_bill.txu_due_date', due[0])

    return True

