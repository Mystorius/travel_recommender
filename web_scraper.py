import sqlite3
from sqlite3 import Error
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

db_path = r"sqlite.db"

'''This section is for web scraping. Because the provided content was not useful, i created my own dataset'''

## create database
def create_db(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        #cursor.execute("""DROP TABLE If exists countries""")
        cursor.execute("""
        CREATE TABLE countries(id INTEGER PRIMARY KEY, name TEXT, about TEXT, area INTEGER, population INTEGER,
        capital TEXT, safety TEXT, terrorism TEXT, entry TEXT, health TEXT, history TEXT, culture TEXT, attractions TEXT,
        shopping TEXT, nightlife TEXT, getting_around TEXT)""")
    except Error as e:
        print(e)
    finally:
        conn.close()
#create_db(db_path)


## insert data into db
def query_db(name1, about1, area1, population1, capital1, safety1, terrorism1, entry1, health1, history1, culture1, attractions1, shopping1, nightlife1, getting_around1):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO countries(name, about, area, population, capital, safety, terrorism, entry, health,
                            history, culture, attractions, shopping, nightlife, getting_around)
                             VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                       ,(name1, about1, area1, population1, capital1, safety1, terrorism1, entry1, health1, history1, culture1,
                         attractions1, shopping1, nightlife1, getting_around1))
        print("inserted data for %s" % name1)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()


## functions for web scrapping
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

all_countries = {'Algeria': 'https://www.worldtravelguide.net/guides/africa/algeria/', 'Angola': 'https://www.worldtravelguide.net/guides/africa/angola/', 'Benin': 'https://www.worldtravelguide.net/guides/africa/benin/', 'Botswana': 'https://www.worldtravelguide.net/guides/africa/botswana/', 'Burkina Faso': 'https://www.worldtravelguide.net/guides/africa/burkina-faso/', 'Burundi': 'https://www.worldtravelguide.net/guides/africa/burundi/', 'Cameroon': 'https://www.worldtravelguide.net/guides/africa/cameroon/', 'Cape Verde': 'https://www.worldtravelguide.net/guides/africa/cape-verde/', 'Central African Republic': 'https://www.worldtravelguide.net/guides/africa/central-african-republic/', 'Chad': 'https://www.worldtravelguide.net/guides/africa/chad/', 'Comoros': 'https://www.worldtravelguide.net/guides/africa/comoros/', 'Democratic Republic of Congo': 'https://www.worldtravelguide.net/guides/africa/democratic-republic-of-congo/', 'Djibouti': 'https://www.worldtravelguide.net/guides/africa/djibouti/', 'Egypt': 'https://www.worldtravelguide.net/guides/africa/egypt/', 'Equatorial Guinea': 'https://www.worldtravelguide.net/guides/africa/equatorial-guinea/', 'Eritrea': 'https://www.worldtravelguide.net/guides/africa/eritrea/', 'Ethiopia': 'https://www.worldtravelguide.net/guides/africa/ethiopia/', 'Gabon': 'https://www.worldtravelguide.net/guides/africa/gabon/', 'Gambia': 'https://www.worldtravelguide.net/guides/africa/gambia/', 'Ghana': 'https://www.worldtravelguide.net/guides/africa/ghana/', 'Guinea': 'https://www.worldtravelguide.net/guides/africa/guinea/', 'Guinea-Bissau': 'https://www.worldtravelguide.net/guides/africa/guinea-bissau/', 'Ivory Coast': 'https://www.worldtravelguide.net/guides/africa/ivory-coast/', 'Kenya': 'https://www.worldtravelguide.net/guides/africa/kenya/', 'Lesotho': 'https://www.worldtravelguide.net/guides/africa/lesotho/', 'Liberia': 'https://www.worldtravelguide.net/guides/africa/liberia/', 'Libya': 'https://www.worldtravelguide.net/guides/africa/libya/', 'Madagascar': 'https://www.worldtravelguide.net/guides/africa/madagascar/', 'Malawi': 'https://www.worldtravelguide.net/guides/africa/malawi/', 'Mali': 'https://www.worldtravelguide.net/guides/africa/mali/', 'Mauritania': 'https://www.worldtravelguide.net/guides/africa/mauritania/', 'Mauritius': 'https://www.worldtravelguide.net/guides/africa/mauritius/', 'Morocco': 'https://www.worldtravelguide.net/guides/africa/morocco/', 'Mozambique': 'https://www.worldtravelguide.net/guides/africa/mozambique/', 'Namibia': 'https://www.worldtravelguide.net/guides/africa/namibia/', 'Niger': 'https://www.worldtravelguide.net/guides/africa/niger/', 'Nigeria': 'https://www.worldtravelguide.net/guides/africa/nigeria/', 'Republic of Congo': 'https://www.worldtravelguide.net/guides/africa/republic-of-congo/', 'Rwanda': 'https://www.worldtravelguide.net/guides/africa/rwanda/', 'São Tomé e Príncipe': 'https://www.worldtravelguide.net/guides/africa/sao-tome-e-principe/', 'Senegal': 'https://www.worldtravelguide.net/guides/africa/senegal/', 'Seychelles': 'https://www.worldtravelguide.net/guides/africa/seychelles/', 'Sierra Leone': 'https://www.worldtravelguide.net/guides/africa/sierra-leone/', 'Somalia': 'https://www.worldtravelguide.net/guides/africa/somalia/', 'South Africa': 'https://www.worldtravelguide.net/guides/africa/south-africa/', 'South Sudan': 'https://www.worldtravelguide.net/guides/africa/south-sudan/', 'Sudan': 'https://www.worldtravelguide.net/guides/africa/sudan/', 'Swaziland': 'https://www.worldtravelguide.net/guides/africa/swaziland/', 'Tanzania': 'https://www.worldtravelguide.net/guides/africa/tanzania/', 'Togo': 'https://www.worldtravelguide.net/guides/africa/togo/', 'Tunisia': 'https://www.worldtravelguide.net/guides/africa/tunisia/', 'Uganda': 'https://www.worldtravelguide.net/guides/africa/uganda/', 'Zambia': 'https://www.worldtravelguide.net/guides/africa/zambia/', 'Zimbabwe': 'https://www.worldtravelguide.net/guides/africa/zimbabwe/', 'Antarctica': 'https://www.worldtravelguide.net/guides/antarctica/antarctica/', 'Armenia': 'https://www.worldtravelguide.net/guides/asia/armenia/', 'Azerbaijan': 'https://www.worldtravelguide.net/guides/asia/azerbaijan/', 'Bangladesh': 'https://www.worldtravelguide.net/guides/asia/bangladesh/', 'Bhutan': 'https://www.worldtravelguide.net/guides/asia/bhutan/', 'Brunei': 'https://www.worldtravelguide.net/guides/asia/brunei/', 'Cambodia': 'https://www.worldtravelguide.net/guides/asia/cambodia/', 'China': 'https://www.worldtravelguide.net/guides/asia/china/', 'East Timor': 'https://www.worldtravelguide.net/guides/asia/east-timor/', 'Georgia': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/georgia-2/', 'Hong Kong': 'https://www.worldtravelguide.net/guides/asia/china/hong-kong/', 'India': 'https://www.worldtravelguide.net/guides/asia/india/', 'Indonesia': 'https://www.worldtravelguide.net/guides/asia/indonesia/', 'Japan': 'https://www.worldtravelguide.net/guides/asia/japan/', 'Kazakhstan': 'https://www.worldtravelguide.net/guides/asia/kazakhstan/', 'Kyrgyzstan': 'https://www.worldtravelguide.net/guides/asia/kyrgyzstan/', 'Laos': 'https://www.worldtravelguide.net/guides/asia/laos/', 'Macau': 'https://www.worldtravelguide.net/guides/asia/china/macau/', 'Malaysia': 'https://www.worldtravelguide.net/guides/asia/malaysia/', 'Maldives': 'https://www.worldtravelguide.net/guides/asia/maldives/', 'Mongolia': 'https://www.worldtravelguide.net/guides/asia/mongolia/', 'Myanmar': 'https://www.worldtravelguide.net/guides/asia/myanmar/', 'Nepal': 'https://www.worldtravelguide.net/guides/asia/nepal/', 'North Korea': 'https://www.worldtravelguide.net/guides/asia/north-korea/', 'Pakistan': 'https://www.worldtravelguide.net/guides/asia/pakistan/', 'Philippines': 'https://www.worldtravelguide.net/guides/asia/philippines/', 'Singapore': 'https://www.worldtravelguide.net/guides/asia/singapore/', 'South Korea': 'https://www.worldtravelguide.net/guides/asia/south-korea/', 'Sri Lanka': 'https://www.worldtravelguide.net/guides/asia/sri-lanka/', 'Taiwan': 'https://www.worldtravelguide.net/guides/asia/taiwan/', 'Tajikistan': 'https://www.worldtravelguide.net/guides/asia/tajikistan/', 'Thailand': 'https://www.worldtravelguide.net/guides/asia/thailand/', 'Tibet': 'https://www.worldtravelguide.net/guides/asia/china/tibet/', 'Turkmenistan': 'https://www.worldtravelguide.net/guides/asia/turkmenistan/', 'Uzbekistan': 'https://www.worldtravelguide.net/guides/asia/uzbekistan/', 'Vietnam': 'https://www.worldtravelguide.net/guides/asia/vietnam/', 'Anguilla': 'https://www.worldtravelguide.net/guides/caribbean/anguilla/', 'Antigua and Barbuda': 'https://www.worldtravelguide.net/guides/caribbean/antigua-and-barbuda/', 'Aruba': 'https://www.worldtravelguide.net/guides/caribbean/aruba/', 'Bahamas': 'https://www.worldtravelguide.net/guides/caribbean/bahamas/', 'Barbados': 'https://www.worldtravelguide.net/guides/caribbean/barbados/', 'Bermuda': 'https://www.worldtravelguide.net/guides/caribbean/bermuda/', 'Bonaire': 'https://www.worldtravelguide.net/guides/caribbean/bonaire/', 'British Virgin Islands': 'https://www.worldtravelguide.net/guides/caribbean/british-virgin-islands/', 'Cayman Islands': 'https://www.worldtravelguide.net/guides/caribbean/cayman-islands/', 'Cuba': 'https://www.worldtravelguide.net/guides/caribbean/cuba/', 'Curaçao': 'https://www.worldtravelguide.net/guides/caribbean/curaao/', 'Dominica': 'https://www.worldtravelguide.net/guides/caribbean/dominica/', 'Dominican Republic': 'https://www.worldtravelguide.net/guides/caribbean/dominican-republic/', 'French Guiana': 'https://www.worldtravelguide.net/guides/caribbean/french-overseas-possessions/french-guiana/', 'French Overseas Possessions': 'https://www.worldtravelguide.net/guides/caribbean/french-overseas-possessions/', 'Grenada': 'https://www.worldtravelguide.net/guides/caribbean/grenada/', 'Guadeloupe': 'https://www.worldtravelguide.net/guides/caribbean/guadeloupe/', 'Haiti': 'https://www.worldtravelguide.net/guides/caribbean/haiti/', 'Jamaica': 'https://www.worldtravelguide.net/guides/caribbean/jamaica/', 'Martinique': 'https://www.worldtravelguide.net/guides/caribbean/martinique/', 'Montserrat': 'https://www.worldtravelguide.net/guides/caribbean/montserrat/', 'Puerto Rico': 'https://www.worldtravelguide.net/guides/caribbean/puerto-rico/', 'Reunion': 'https://www.worldtravelguide.net/guides/caribbean/french-overseas-possessions/reunion/', 'Saba': 'https://www.worldtravelguide.net/guides/caribbean/saba/', 'St Eustatius': 'https://www.worldtravelguide.net/guides/caribbean/st-eustatius/', 'St Kitts And Nevis': 'https://www.worldtravelguide.net/guides/caribbean/st-kitts-and-nevis/', 'St Lucia': 'https://www.worldtravelguide.net/guides/caribbean/st-lucia/', 'St Maarten': 'https://www.worldtravelguide.net/guides/caribbean/st-maarten/', 'St Vincent and the Grenadines': 'https://www.worldtravelguide.net/guides/caribbean/st-vincent-and-the-grenadines/', 'Trinidad and Tobago': 'https://www.worldtravelguide.net/guides/caribbean/trinidad-and-tobago/', 'Turks and Caicos Islands': 'https://www.worldtravelguide.net/guides/caribbean/turks-and-caicos-islands/', 'US Virgin Islands': 'https://www.worldtravelguide.net/guides/caribbean/us-virgin-islands/', 'Albania': 'https://www.worldtravelguide.net/guides/europe/albania/', 'Alderney': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/channel-islands/alderney/', 'Andorra': 'https://www.worldtravelguide.net/guides/europe/andorra/', 'Austria': 'https://www.worldtravelguide.net/guides/europe/austria/', 'Azores': 'https://www.worldtravelguide.net/guides/europe/portugal/azores/', 'Balearic Islands': 'https://www.worldtravelguide.net/guides/europe/spain/balearic-islands/', 'Belarus': 'https://www.worldtravelguide.net/guides/europe/belarus/', 'Belgium': 'https://www.worldtravelguide.net/guides/europe/belgium/', 'Bosnia and Herzegovina': 'https://www.worldtravelguide.net/guides/europe/bosnia-and-herzegovina/', 'British Overseas Territories': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/british-overseas-territories/', 'Bulgaria': 'https://www.worldtravelguide.net/guides/europe/bulgaria/', 'Canary Islands': 'https://www.worldtravelguide.net/guides/europe/spain/canary-islands/', 'Channel Islands': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/channel-islands/', 'Croatia': 'https://www.worldtravelguide.net/guides/europe/croatia/', 'Cyprus': 'https://www.worldtravelguide.net/guides/europe/cyprus/', 'Czech Republic': 'https://www.worldtravelguide.net/guides/europe/czech-republic/', 'Denmark': 'https://www.worldtravelguide.net/guides/europe/denmark/', 'England': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/england/', 'Estonia': 'https://www.worldtravelguide.net/guides/europe/estonia/', 'Finland': 'https://www.worldtravelguide.net/guides/europe/finland/', 'France': 'https://www.worldtravelguide.net/guides/europe/france/', 'Germany': 'https://www.worldtravelguide.net/guides/europe/germany/', 'Gibraltar': 'https://www.worldtravelguide.net/guides/europe/gibraltar/', 'Gran Canaria': 'https://www.worldtravelguide.net/guides/europe/spain/canary-islands/gran-canaria/', 'Greece': 'https://www.worldtravelguide.net/guides/europe/greece/', 'Guernsey': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/channel-islands/guernsey/', 'Hungary': 'https://www.worldtravelguide.net/guides/europe/hungary/', 'Ibiza': 'https://www.worldtravelguide.net/guides/europe/spain/balearic-islands/ibiza/', 'Iceland': 'https://www.worldtravelguide.net/guides/europe/iceland/', 'Ireland': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/ireland/', 'Isle of Man': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/isle-of-man/', 'Italy': 'https://www.worldtravelguide.net/guides/europe/italy/', 'Jersey': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/channel-islands/jersey/', 'Kosovo': 'https://www.worldtravelguide.net/guides/europe/kosovo/', 'Lanzarote': 'https://www.worldtravelguide.net/guides/europe/spain/canary-islands/lanzarote/', 'Latvia': 'https://www.worldtravelguide.net/guides/europe/latvia/', 'Liechtenstein': 'https://www.worldtravelguide.net/guides/europe/liechtenstein/', 'Lithuania': 'https://www.worldtravelguide.net/guides/europe/lithuania/', 'Luxembourg': 'https://www.worldtravelguide.net/guides/europe/luxembourg/', 'Macedonia': 'https://www.worldtravelguide.net/guides/europe/macedonia/', 'Madeira': 'https://www.worldtravelguide.net/guides/europe/portugal/madeira/', 'Mallorca': 'https://www.worldtravelguide.net/guides/europe/spain/balearic-islands/mallorca/', 'Malta': 'https://www.worldtravelguide.net/guides/europe/malta/', 'Menorca': 'https://www.worldtravelguide.net/guides/europe/spain/balearic-islands/menorca/', 'Moldova': 'https://www.worldtravelguide.net/guides/europe/moldova/', 'Monaco': 'https://www.worldtravelguide.net/guides/europe/monaco/', 'Montenegro': 'https://www.worldtravelguide.net/guides/europe/montenegro/', 'Netherlands': 'https://www.worldtravelguide.net/guides/europe/netherlands/', 'Northern Ireland': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/northern-ireland/', 'Norway': 'https://www.worldtravelguide.net/guides/europe/norway/', 'Poland': 'https://www.worldtravelguide.net/guides/europe/poland/', 'Portugal': 'https://www.worldtravelguide.net/guides/europe/portugal/', 'Romania': 'https://www.worldtravelguide.net/guides/europe/romania/', 'Russia': 'https://www.worldtravelguide.net/guides/europe/russia/', 'San Marino': 'https://www.worldtravelguide.net/guides/europe/san-marino/', 'Sark & Herm': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/channel-islands/sark-herm/', 'Scotland': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/scotland/', 'Serbia': 'https://www.worldtravelguide.net/guides/europe/serbia/', 'Slovakia': 'https://www.worldtravelguide.net/guides/europe/slovakia/', 'Slovenia': 'https://www.worldtravelguide.net/guides/europe/slovenia/', 'Spain': 'https://www.worldtravelguide.net/guides/europe/spain/', 'Sweden': 'https://www.worldtravelguide.net/guides/europe/sweden/', 'Switzerland': 'https://www.worldtravelguide.net/guides/europe/switzerland/', 'Tenerife': 'https://www.worldtravelguide.net/guides/europe/spain/canary-islands/tenerife/', 'Turkey': 'https://www.worldtravelguide.net/guides/europe/turkey/', 'Ukraine': 'https://www.worldtravelguide.net/guides/europe/ukraine/', 'United Kingdom': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/', 'Vatican City': 'https://www.worldtravelguide.net/guides/europe/vatican-city/', 'Wales': 'https://www.worldtravelguide.net/guides/europe/united-kingdom/wales/', 'Afghanistan': 'https://www.worldtravelguide.net/guides/middle-east/afghanistan/', 'Bahrain': 'https://www.worldtravelguide.net/guides/middle-east/bahrain/', 'Iran': 'https://www.worldtravelguide.net/guides/middle-east/iran/', 'Iraq': 'https://www.worldtravelguide.net/guides/middle-east/iraq/', 'Israel': 'https://www.worldtravelguide.net/guides/middle-east/israel/', 'Jordan': 'https://www.worldtravelguide.net/guides/middle-east/jordan/', 'Kuwait': 'https://www.worldtravelguide.net/guides/middle-east/kuwait/', 'Lebanon': 'https://www.worldtravelguide.net/guides/middle-east/lebanon/', 'Oman': 'https://www.worldtravelguide.net/guides/middle-east/oman/', 'Palestinian National Authority': 'https://www.worldtravelguide.net/guides/middle-east/palestinian-national-authority/', 'Qatar': 'https://www.worldtravelguide.net/guides/middle-east/qatar/', 'Saudi Arabia': 'https://www.worldtravelguide.net/guides/middle-east/saudi-arabia/', 'Syrian Arab Republic': 'https://www.worldtravelguide.net/guides/middle-east/syrian-arab-republic/', 'United Arab Emirates': 'https://www.worldtravelguide.net/guides/middle-east/united-arab-emirates/', 'Yemen': 'https://www.worldtravelguide.net/guides/middle-east/yemen/', 'Alabama': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/alabama/', 'Alaska': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/alaska/', 'Alberta': 'https://www.worldtravelguide.net/guides/north-america/canada/alberta/', 'Arizona': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/arizona/', 'Arkansas': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/arkansas/', 'Belize': 'https://www.worldtravelguide.net/guides/north-america/belize/', 'British Columbia': 'https://www.worldtravelguide.net/guides/north-america/canada/british-columbia/', 'California': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/california/', 'Canada': 'https://www.worldtravelguide.net/guides/north-america/canada/', 'Colorado': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/colorado/', 'Connecticut': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/connecticut/', 'Costa Rica': 'https://www.worldtravelguide.net/guides/north-america/costa-rica/', 'Delaware': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/delaware/', 'El Salvador': 'https://www.worldtravelguide.net/guides/north-america/el-salvador/', 'Florida': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/florida/', 'Greenland': 'https://www.worldtravelguide.net/guides/north-america/greenland/', 'Guatemala': 'https://www.worldtravelguide.net/guides/north-america/guatemala/', 'Hawaii': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/hawaii/', 'Honduras': 'https://www.worldtravelguide.net/guides/north-america/honduras/', 'Idaho': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/idaho/', 'Illinois': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/illinois/', 'Indiana': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/indiana/', 'Iowa': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/iowa/', 'Kansas': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/kansas/', 'Kentucky': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/kentucky/', 'Louisiana': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/louisiana/', 'Maine': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/maine/', 'Manitoba': 'https://www.worldtravelguide.net/guides/north-america/canada/manitoba/', 'Maryland': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/maryland/', 'Massachusetts': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/massachusetts/', 'Mexico': 'https://www.worldtravelguide.net/guides/north-america/mexico/', 'Michigan': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/michigan/', 'Minnesota': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/minnesota/', 'Mississippi': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/mississippi/', 'Missouri': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/missouri/', 'Montana': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/montana/', 'Nebraska': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/nebraska/', 'Nevada': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/nevada/', 'New Brunswick': 'https://www.worldtravelguide.net/guides/north-america/canada/new-brunswick/', 'New Hampshire': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/new-hampshire/', 'New Jersey': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/new-jersey/', 'New Mexico': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/new-mexico/', 'New York State': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/new-york-state/', 'Newfoundland And Labrador': 'https://www.worldtravelguide.net/guides/north-america/canada/newfoundland-and-labrador/', 'Nicaragua': 'https://www.worldtravelguide.net/guides/north-america/nicaragua/', 'North Carolina': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/north-carolina/', 'North Dakota': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/north-dakota/', 'Northwest Territories': 'https://www.worldtravelguide.net/guides/north-america/canada/northwest-territories/', 'Nova Scotia': 'https://www.worldtravelguide.net/guides/north-america/canada/nova-scotia/', 'Nunavut': 'https://www.worldtravelguide.net/guides/north-america/canada/nunavut/', 'Ohio': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/ohio/', 'Oklahoma': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/oklahoma/', 'Ontario': 'https://www.worldtravelguide.net/guides/north-america/canada/ontario/', 'Oregon': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/oregon/', 'Panama': 'https://www.worldtravelguide.net/guides/north-america/panama/', 'Pennsylvania': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/pennsylvania/', 'Prince Edward Island': 'https://www.worldtravelguide.net/guides/north-america/canada/prince-edward-island/', 'Quebec': 'https://www.worldtravelguide.net/guides/north-america/canada/quebec/', 'Rhode Island': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/rhode-island/', 'Saskatchewan': 'https://www.worldtravelguide.net/guides/north-america/canada/saskatchewan/', 'South Carolina': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/south-carolina/', 'South Dakota': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/south-dakota/', 'Tennessee': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/tennessee/', 'Texas': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/texas/', 'United States of America': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/', 'Utah': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/utah/', 'Vermont': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/vermont/', 'Virginia': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/virginia/', 'Washington State': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/washington-state/', 'West Virginia': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/west-virginia/', 'Wisconsin': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/wisconsin/', 'Wyoming': 'https://www.worldtravelguide.net/guides/north-america/united-states-of-america/wyoming/', 'Yukon Territory': 'https://www.worldtravelguide.net/guides/north-america/canada/yukon-territory/', 'American Samoa': 'https://www.worldtravelguide.net/guides/oceania/american-samoa/', 'Australia': 'https://www.worldtravelguide.net/guides/oceania/australia/', 'Australian Capital Territory': 'https://www.worldtravelguide.net/guides/oceania/australia/australian-capital-territory/', 'Cook Islands': 'https://www.worldtravelguide.net/guides/oceania/cook-islands/', 'Federated States Of Micronesia': 'https://www.worldtravelguide.net/guides/oceania/pacific-islands-of-micronesia/federated-states-of-micronesia/', 'Fiji': 'https://www.worldtravelguide.net/guides/oceania/fiji/', 'Guam': 'https://www.worldtravelguide.net/guides/oceania/guam/', 'Kiribati': 'https://www.worldtravelguide.net/guides/oceania/kiribati/', 'Marshall Islands': 'https://www.worldtravelguide.net/guides/oceania/pacific-islands-of-micronesia/marshall-islands/', 'Nauru': 'https://www.worldtravelguide.net/guides/oceania/nauru/', 'New Caledonia': 'https://www.worldtravelguide.net/guides/oceania/new-caledonia/', 'New South Wales': 'https://www.worldtravelguide.net/guides/oceania/australia/new-south-wales/', 'New Zealand': 'https://www.worldtravelguide.net/guides/oceania/new-zealand/', 'Niue': 'https://www.worldtravelguide.net/guides/oceania/niue/', 'Northern Mariana Islands': 'https://www.worldtravelguide.net/guides/oceania/pacific-islands-of-micronesia/northern-mariana-islands/', 'Northern Territory': 'https://www.worldtravelguide.net/guides/oceania/australia/northern-territory/', 'Pacific Islands Of Micronesia': 'https://www.worldtravelguide.net/guides/oceania/pacific-islands-of-micronesia/', 'Palau': 'https://www.worldtravelguide.net/guides/oceania/pacific-islands-of-micronesia/palau/', 'Papua New Guinea': 'https://www.worldtravelguide.net/guides/oceania/papua-new-guinea/', 'Queensland': 'https://www.worldtravelguide.net/guides/oceania/australia/queensland/', 'Samoa': 'https://www.worldtravelguide.net/guides/oceania/samoa/', 'Solomon Islands': 'https://www.worldtravelguide.net/guides/oceania/solomon-islands/', 'South Australia': 'https://www.worldtravelguide.net/guides/oceania/australia/south-australia/', 'Tahiti and her Islands': 'https://www.worldtravelguide.net/guides/oceania/tahiti-and-her-islands/', 'Tasmania': 'https://www.worldtravelguide.net/guides/oceania/australia/tasmania/', 'Tonga': 'https://www.worldtravelguide.net/guides/oceania/tonga/', 'Tuvalu': 'https://www.worldtravelguide.net/guides/oceania/tuvalu/', 'Vanuatu': 'https://www.worldtravelguide.net/guides/oceania/vanuatu/', 'Victoria': 'https://www.worldtravelguide.net/guides/oceania/australia/victoria/', 'Western Australia': 'https://www.worldtravelguide.net/guides/oceania/australia/western-australia/', 'Argentina': 'https://www.worldtravelguide.net/guides/south-america/argentina/', 'Bolivia': 'https://www.worldtravelguide.net/guides/south-america/bolivia/', 'Brazil': 'https://www.worldtravelguide.net/guides/south-america/brazil/', 'Chile': 'https://www.worldtravelguide.net/guides/south-america/chile/', 'Colombia': 'https://www.worldtravelguide.net/guides/south-america/colombia/', 'Ecuador': 'https://www.worldtravelguide.net/guides/south-america/ecuador/', 'Falkland Islands': 'https://www.worldtravelguide.net/guides/south-america/falkland-islands/', 'Guyana': 'https://www.worldtravelguide.net/guides/south-america/guyana/', 'Paraguay': 'https://www.worldtravelguide.net/guides/south-america/paraguay/', 'Peru': 'https://www.worldtravelguide.net/guides/south-america/peru/', 'Surinam': 'https://www.worldtravelguide.net/guides/south-america/surinam/', 'Uruguay': 'https://www.worldtravelguide.net/guides/south-america/uruguay/', 'Venezuela': 'https://www.worldtravelguide.net/guides/south-america/venezuela/'}

## function to get all links (seen above in the dict)
def get_links():
    all_countries = {}
    path = "https://www.worldtravelguide.net/country-guides/"
    raw_html = simple_get(path)
    html = BeautifulSoup(raw_html, "html.parser")
    links = html.find("div", {"class": "tab-content"})
    # print(links)
    for link in links.select("li"):
        if "Select your country" not in link.text:
            for a in link.select("a"):
                all_countries[link.text] = a.get("href")

## get content from every page, parse it, and write it to db
for country in all_countries:
    country_dict = {"about": "",
                    "key_facts": {"area": "", "population": "", "capital": ""},
                    "travel_advice": {"safety": "", "terrorism": "", "entry": "", "health": ""},
                    "history": "",
                    "culture": "",
                    "attractions": "",
                    "shopping": "",
                    "nightlife": "",
                    "getting_around": ""
                    }
    link = all_countries[country]


    def about_page():
        def parse_about():
            raw_txt = ""
            for p in about.select("p"):
                if "sq miles" in p.text:
                    break
                else:
                    raw_txt += (p.text + " ")
            country_dict["about"] = raw_txt

        def parse_key_facts():
            for div in key_facts.select("div"):
                if "Area:" in div.text:
                    for p in div.select("p"):
                        country_dict["key_facts"]["area"] = p.text
                if "Population" in div.text:
                    for p in div.select("p"):
                        country_dict["key_facts"]["population"] = p.text
                if "Capital" in div.text:
                    for p in div.select("p"):
                        country_dict["key_facts"]["capital"] = p.text

        def parse_travel_advice():
            for div in travel_advice.select("div"):
                for section in div.select("section"):
                    if "Safety and security" in section.text:
                        raw_txt = ""
                        for p in section.select("p"):
                            raw_txt += (p.text + " ")
                        country_dict["travel_advice"]["safety"] = raw_txt
                    if "Terrorism" in section.text:
                        raw_txt = ""
                        for p in section.select("p"):
                            raw_txt += (p.text + " ")
                        country_dict["travel_advice"]["terrorism"] = raw_txt
                    if "Entry requirements" in section.text:
                        raw_txt = ""
                        for p in section.select("p"):
                            raw_txt += (p.text + " ")
                        country_dict["travel_advice"]["entry"] = raw_txt
                    if "Health" in section.text:
                        raw_txt = ""
                        for p in section.select("p"):
                            raw_txt += (p.text + " ")
                        country_dict["travel_advice"]["health"] = raw_txt

        path = link
        raw_html = simple_get(path)
        html = BeautifulSoup(raw_html, "html.parser")

        try:
            about = html.find("div", {"xmlns:fn": "http://www.w3.org/2005/xpath-functions","itemprop": "text" })
            parse_about()
        except:
            print("no about in %s" % country)
        try:
            key_facts = html.find("div", {"class": "keyfacts"})
            parse_key_facts()
        except:
            print("no key facts in %s" % country)
        try:
            travel_advice = html.find("div", {"class": "travel_advice"})
            parse_travel_advice()
        except:
            print("no travel advice in %s" % country)


    def history_page():
        def parse_history():
            raw_txt = ""
            for h2 in history.select("h2"):
                if "History of " in h2.text:
                    raw_txt += h2.find_next_sibling("p").text
            country_dict["history"] = raw_txt

        def parse_culture():
            raw_txt = ""
            for h3 in culture.select("h3"):
                if "Religion in " in h3.text:
                    raw_txt += h3.nextSibling.text
                elif "Social Conventions in " in h3.text:
                    raw_txt += h3.nextSibling.text
            country_dict["culture"] = raw_txt

        path = "{}{}".format(link, "/history-language-culture/")
        raw_html = simple_get(path)
        html = BeautifulSoup(raw_html, "html.parser")
        try:
            history = html.find("article", {"class": "col-md-7 col-sm-7 main_content", "itemtype": "https://schema.org/CreativeWork"})
            parse_history()
        except:
            print("no history in %s" % country)
        try:
            culture = html.find("article",{"class": "col-md-7 col-sm-7 main_content", "itemtype": "https://schema.org/CreativeWork"})
            parse_culture()
        except:
            print("no culture in %s" % country)


    def attractions_page():
        def parse_attractions():
            raw_txt = ""
            for p in attractions.select("p"):
                raw_txt += (p.text + " ")
            country_dict["attractions"] = raw_txt

        path = "{}{}".format(link, "/things-to-do/")
        raw_html = simple_get(path)
        html = BeautifulSoup(raw_html, "html.parser")

        try:
            attractions = html.find("article", {"class": "col-md-7 col-sm-7 main_content", "itemtype": "https://schema.org/CreativeWork"})
            parse_attractions()
        except:
            print("no attractions in %s" % country)


    def shopping_nightlife_page():
        def parse_shopping():
            raw_txt = ""
            for h2 in shopping.select("h2"):
                if "Nightlife in " in h2.text:
                    stop = h2.nextSibling.text

            for p in shopping.select("p"):
                if stop in p.text:
                    break
                else:
                    raw_txt += (p.text + " ")
            country_dict["shopping"] = raw_txt

        def parse_nightlife():
            raw_txt = ""
            for h2 in nightlife.select("h2"):
                if "Nightlife in " in h2.text:
                    raw_txt += h2.find_next_sibling("p").text
            country_dict["nightlife"] = raw_txt

        path = "{}{}".format(link, "/shopping-nightlife/")
        raw_html = simple_get(path)
        html = BeautifulSoup(raw_html, "html.parser")

        try:
            shopping = html.find("article", {"class": "col-md-7 col-sm-7 main_content", "itemtype": "https://schema.org/CreativeWork"})
            parse_shopping()
        except:
            print("no shopping in %s" % country)

        try:
            nightlife = html.find("article", {"class": "col-md-7 col-sm-7 main_content", "itemtype": "https://schema.org/CreativeWork"})
            parse_nightlife()
        except:
            print("no nightlife in %s" % country)


    def getting_around():
        def parse_getting_around():
            raw_txt = ""
            for p in getting_around.select("p"):
                    raw_txt += (p.text + " ")
            country_dict["getting_around"] = raw_txt

        path = "{}{}".format(link, "/getting-around/")
        raw_html = simple_get(path)
        html = BeautifulSoup(raw_html, "html.parser")

        try:
            getting_around = html.find("article", {"class": "col-md-7 col-sm-7 main_content", "itemtype": "https://schema.org/CreativeWork"})
            parse_getting_around()
        except:
            print("no attractions in %s" % country)


    about_page()
    history_page()
    attractions_page()
    shopping_nightlife_page()
    getting_around()

    query_db(country,
             country_dict["about"],
             country_dict["key_facts"]["area"],
             country_dict["key_facts"]["population"],
             country_dict["key_facts"]["capital"],
             country_dict["travel_advice"]["safety"],
             country_dict["travel_advice"]["terrorism"],
             country_dict["travel_advice"]["entry"],
             country_dict["travel_advice"]["health"],
             country_dict["history"],
             country_dict["culture"],
             country_dict["attractions"],
             country_dict["shopping"],
             country_dict["nightlife"],
             country_dict["getting_around"],)
