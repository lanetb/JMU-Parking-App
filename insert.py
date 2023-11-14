#Attempt to convert data to a mysql database in order to restore this apps functionality unscuccessful so far 
import csv
import pymysql

def get_db():
    #con = psycopg2.connect('host=localhost dbname=outliers user=outliers password=83LXyS4!2wN#pn!-')
    #con = psycopg2.connect('host=data.cs.jmu.edu dbname=outliers user=outliers password=83LXyS4!2wN#pn!-')
    con = 0
    return con

def main():
    con = get_db()
    cur = con.cursor()

    # Read in the data from decks.csv
    #with open('./schema/decks.csv', newline='') as csvfile:
    #    print("Inserting data into decks table")
    #    reader = csv.reader(csvfile)
    #    next(reader)  # Skip the header row
    #    for row in reader:
    #        # Construct the INSERT statement
    #        insert_stmt = "INSERT INTO decks (deck_name, deck_id, address, latitude, longitude) VALUES ('{}', '{}', '{}', '{}', '{}')".format(row[0], row[1], row[2], row[3], row[4])
    #        # Execute the INSERT statement
    #        cur.execute(insert_stmt)
    #    print("Finished inserting data into decks table")

    # Read in the data from buildings.csv
    #with open('./schema/buildings.csv', newline='') as csvfile:
    #    print("Inserting data into buildings table")
    #    reader = csv.reader(csvfile)
    #    next(reader)  # Skip the header row
    #    for row in reader:
    #        # Construct the INSERT statement
    #        insert_stmt = "INSERT INTO buildings (building_name, building_id, address, latitude, longitude) VALUES ('{}', '{}', '{}', '{}', '{}')".format(row[0], row[1], row[2], row[3], row[4])
    #        # Execute the INSERT statement
    #        cur.execute(insert_stmt)
    #        # Execute the INSERT statement
    #        cur.execute(insert_stmt)
    #    print("Finished inserting data into buildings table")
    
    # Read in the data from distances.csv
    #with open('./schema/distances.csv', newline='') as csvfile:
    #    print("Inserting data into distances table")
    #    reader = csv.reader(csvfile)
    #    next(reader)  # Skip the header row
    #    for row in reader:
    #        # Construct the INSERT statement
    #        insert_stmt = "INSERT INTO distances (minutes, distance, deck_id, building_id, distance_id) VALUES ('{}', '{}', '{}', '{}', '{}')".format(row[0], row[1], row[2], row[3], row[4])
    #        # Execute the INSERT statement
    #        cur.execute(insert_stmt)
    #    print("Finished inserting data into distances table")

    # Read in the data from meetings.csv
    #with open('./schema/meetings.csv', newline='') as csvfile:
    #    print("Inserting data into meetings table")
    #    reader = csv.reader(csvfile)
    #    count = 0
    #    next(reader)  # Skip the header row
    #    for row in reader:
    #        count += 1
    #        print(count)
    #        # Construct the INSERT statement

    #        insert_stmt = "INSERT INTO meetings (course_nbr, term , days, start_t, end_t, enrolled, building_id, meeting_id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    #        # Execute the INSERT statement
    #        try:
    #            cur.execute(insert_stmt)
    #        except:
    #            print("Error: Could not insert data into meetings table. Reconnecting...")
    #            con = get_db()
    #            cur = con.cursor()
    #            cur.execute(insert_stmt)
    #            print("Reconnected: Inserting data into meetings table")
    #    print("Finished inserting data into meetings table")

    # Read in the data from observations.csv
    with open('./schema/observations.csv', newline='') as csvfile:
        print("Inserting data into observations table")
        reader = csv.reader(csvfile)
        count = 0
        next(reader)  # Skip the header row
        for row in reader:
            count += 1
            print('%d\r'%count, end="")
            # Construct the INSERT statement
            insert_stmt = "INSERT INTO observations (date_time, type, occ, deck_id, obs_id) VALUES ('{}', '{}', '{}', '{}', '{}')".format(row[0], row[1], row[2], row[3], row[4])
            # Execute the INSERT statement
            try:
                cur.execute(insert_stmt)
            except:
                print("Error: Could not insert data into observations table. Reconnecting...")
                con = get_db()
                cur = con.cursor()
                cur.execute(insert_stmt)
                print("Reconnected: Inserting data into observations table")
        print("Finished inserting data into observations table")
    
    # Read in the data from terms.csv
    #with open('./schema/terms.csv', newline='') as csvfile:
    #    print("Inserting data into terms table")
    #    reader = csv.reader(csvfile)
    #    next(reader)  # Skip the header row
    #    for row in reader:
    #        # Construct the INSERT statement
    #        insert_stmt = "INSERT INTO terms (term, start_date, end_date) VALUES ('{}', '{}', '{}')".format(row[0], row[1], row[2])
    #        # Execute the INSERT statement
    #        cur.execute(insert_stmt)
    #    print("Finished inserting data into terms table")

    con.commit()
    con.close()

if __name__ == "__main__":
    main()

    