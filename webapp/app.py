from datetime import datetime
import certifi
import ssl
import geopy
from flask import Flask, render_template, request
import psycopg2
import pymysql

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

app = Flask(__name__)


# Gets a list of building names from the building table. This is used by the building selector on home_page.html
get_buildings_list_sql = """
SELECT building_name
FROM buildings;
"""

# Gets a list of deck names from the deck table. This is used by the deck selector on home_page.html
get_decks_list_sql = """
SELECT deck_name
FROM decks;
"""

# Gets all the data from the decks table
get_decks_sql = """
SELECT *
FROM decks;
"""


# Get the database connection. One con assignment needs to be commented out depending on if the database is being
# accessed from on campus or if it is being accessed from off campus
def get_db():
    con = 0
    return con

# The home page
@app.route('/')
def home():
    # Request arguments
    timestamp = request.args.get('timestamp', '')
    building = request.args.get('building', '')
    deck = request.args.get('deck', '')
    distance = request.args.get('distance', '')
    max_number = request.args.get('max_number', '')

    # Get the database connection and cursor
    con = get_db()
    cur = con.cursor()

    # Get and store the decks table (deck_name, deck_id, address, latitude, longitude) in the decks list. The decks list
    # holds info about all the decks that should be rendered on the map. Since the map initially renders all of the
    # decks it should initially hold data about all of them.
    cur.execute(get_decks_sql)
    decks = cur.fetchall()

    # Call the closest_deck function to get and store a table with
    # (building_name, building_latitude, building_longitude, building_address, deck_id, minutes, distance, building_id)
    # in the buildings list. The buildings list holds info about all the buildings that should be rendered on the map.
    # Since the map initially renders all of the buildings it should initially hold data about all of them.
    cur.callproc("closest_deck")
    buildings = cur.fetchall()

    # Get a list of building names from the buildings table for use in the building selector
    cur.execute(get_buildings_list_sql)
    buildings_list = cur.fetchall()

    # Get a list of deck names from the decks table for use in the deck selector
    cur.execute(get_decks_list_sql)
    decks_list = cur.fetchall()

    # Will hold the number of filled commuter spaces in each deck at the observation closest to the timestamp argument
    # key: deck_id, value: occupancy
    deck_occupancies = {}

    # Will hold the number of people enrolled in a class in each building at a the timestamp argument
    # key: building_id, value: enrolled
    building_occupancies = {}

    # If the distance and deck arguments are passed this will hold the table returned by the buildings within distance
    # function which gets data on all the buildings within a given distance of a given deck
    # (building_name, distance, minutes)
    buildings_in_dist = None

    # If the max_number and deck arguments are passed this will hold the table returned by the closest buildings
    # function which gets data on a given number of closest buildings to a given deck
    # (building_name, distance, minutes)
    num_closest_buildings = None

    # If the building paramater is passed find that building in the buildings list and set the buildings list to a list
    # containing info about just that building so that it is the only one that renders on the map
    if building:
        for row in buildings:
            if row[0] == building:
                buildings = [row]
                break

    # If the deck paramater is passed find that deck in the decks list and set the decks list to a list containing info
    # about just that deck so that it is the only one that renders on the map
    if deck:
        for row in decks:
            if row[0] == deck:
                decks = [row]
                break

    # If the distance and deck paramaters are both passed and the building paramater is not, set the buildings list to a
    # list that holds data about all the buildings within the distance paramater of the deck paramater. This code does
    # not execute if the building paramater is set because if an individual building is selected it takes priority over
    # this function, and only that building should be renderred on the map.
    if distance and (deck and deck != 'None') and (not building or building == "None"):

        # Call the buildings within distance function and store the table in the buildings_in_dist list
        # (building_name, distance, minutes)
        cur.callproc('buildings_within_distance', [deck, distance])
        buildings_in_dist = cur.fetchall()

        # A temporary list that stores all the rows from the buildings list that correspond with rows from the
        # buildings_in_dist list
        buildings_temp = []

        # Iterate through the buildings list and buildings_in_dist list and store all the rows from the buildings list
        # that correspond to the buildings_in_dist list in the buildings_temp list.
        for a in buildings:
            for b in buildings_in_dist:
                if b[0] == a[0]:
                    buildings_temp.append(a)

        # Set the buildings list to the buildings_temp list so that only the buildings within the distance paramater of
        # the deck paramater are rendered on the map.
        buildings = buildings_temp

    # If the max_number and deck paramaters are both passed and the building paramater is not, set the buildings list to
    # a list that holds data about the closest max_num paramater of buildings to the deck paramater. This code does
    # not execute if the building paramater is set because if an individual building is selected it takes priority over
    # this function, and only that building should be rendered on the map. If both the max_number and distance
    # paramaters are set then only buildings that meet both filters will be rendered
    if max_number and (deck and deck != 'None') and (not building or building == "None"):

        # Call the closest buildings function and store the table in the num_closest_buildings list
        # (building_name, distance, minutes)
        cur.callproc('closest_buildings', [deck, max_number])
        num_closest_buildings = cur.fetchall()

        # A temporary list that stores all the rows from the buildings list that correspond with rows from the
        # num_closest_buildings list
        buildings_temp = []

        # Iterate through the buildings list and num_closest_buildings list and store all the rows from the buildings
        # list that correspond to the num_closest_buildings list in the buildings_temp list.
        for a in buildings:
            for b in num_closest_buildings:
                if b[0] == a[0]:
                    buildings_temp.append(a)

        # Set the buildings list to the buildings_temp list so that only max_num paramater of buildings closest to the
        # the deck paramater are rendered on the map.
        buildings = buildings_temp

    # If the timestamp paramater is passed get the occupancy of each deck at the nearest observation, and the number of
    # students enrolled in a class in each building at the timestamp.
    if timestamp:

        # Convert the timestamp to a date time object and get the day of the week
        date_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M')
        weekday = date_time.weekday()

        # day is the abbreviation for the day of the week of date passed to the occupancy at date time function. It is
        # initialized to a value that will never appear in the days field of the meetings table.
        day = '%Q%'

        # Set day to the abbreviation corresponding with the day extracted from the date time object derived from the
        # timestamp paramater. The abbreviation is enclosed by percent signs because the function uses the like operator
        # on it to see if the specific day appears in the days field. (Ex. TUTH contains TU). S is for saturday because
        # there are no classes in our database on sundays.
        if weekday == 0:
            day = '%M%'
        elif weekday == 1:
            day = '%TU%'
        elif weekday == 2:
            day = '%W%'
        elif weekday == 3:
            day = '%TH%'
        elif weekday == 4:
            day = '%F%'
        elif weekday == 5:
            day = '%S%'

        # Call the occupancy at date time each building function and pass it the date and time from date_time and the
        # day abbreviation that we set. Store the resulting table in building_occupancies_tup. (building_id, occupancy).
        cur.callproc('occupancy_date_time_each_building', [date_time.date(), date_time.time(), day])
        building_occupancies_tup = cur.fetchall()

        # Convert the building_occupancies_tup list to a dict to be used by the map
        building_occupancies = dict(building_occupancies_tup)

        # Iterate through all of the decks and use the deck_occupancy function to get each of their occupancies at the
        # observation time closest to the timestamp paramater and store them in the deck_occupancies dict
        for val in decks:
            cur.callproc('deck_occupancy', [val[1], timestamp])
            occ = cur.fetchone()

            # Check that the function returned data (This is necessary right now becuase we haven't entered parking data
            # for each deck in our decks table into the observations table.)
            if occ:
                deck_occupancies[val[1]] = occ[0]

    # Close the cursor and the connection
    cur.close()
    con.close()

    # Render home_page.html and pass it all the data that we got for it to use
    return render_template('home_page.html', buildings=buildings, decks=decks, timestamp=timestamp,
                           deck_occupancies=deck_occupancies, building_occupancies=building_occupancies,
                           buildings_list=buildings_list, building=building, decks_list=decks_list, deck=deck,
                           distance=distance, max_number=max_number, buildings_in_dist=buildings_in_dist,
                           num_closest_buildings=num_closest_buildings)

#analysis page
@app.route('/occupancy_at_date_time')
def charts():
    date = request.args.get('date', '')
    deck = request.args.get('deck', '')

    con = get_db()
    cur = con.cursor()

    cur.execute(get_decks_sql)
    decks = cur.fetchall()

    if not date or deck == '' or not deck:
         cur.close()
         con.close()
         return render_template('deck_over_day_form.html', decks=decks)
    else:
         print(date)
         print(deck)
         cur.callproc('deck_occ_during_day', [date, deck])
         dat = cur.fetchall()
         cur.close()
         con.close()
         return render_template('deck_over_day_chart.html', dat=dat, date=date, decks=decks)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
