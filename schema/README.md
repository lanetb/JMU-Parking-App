# STEPS TO CREATE DATABASE

1. Obtain parking and enrollment data from data.cs.jmu.edu and Dr. Mayfield.

2. Get only the columns we need from enrollment data.

3. Filter out irrelevant enrollment data. (Null values, TBA information, Online classes, study abroad classes, upark classes, old buildings).

4. Get and clean the building names from the room number column for enrollment data.

6. Create a building table with all the buildings in our enrollment data and assign them an id.

7. Replace the building name in enrollment data with the building ids from the building table.

8. Create a deck table with all the decks we have data for.

9. Create a new csv file called distance and make rows for each parking deck to every building on campus using keys for building and deck and add the time in minutes and distance it would take to walk.

11. Remove the deck name column from each observation.

12. Combine all the observations into 1 table

13. Run create.sql to create tables with group ownership.

14. Run copy.sh on data.cs.jmu.edu to copy data from the csv files.

15. Run alter.sql to add PRIMARY/FOREIGN key constraints.

16. Run index.sql to create indexes on specific tables.

17. Run stats.sql to count rows and analyze the tables.

```bash
export PGHOST=data.cs.jmu.edu
export PGDATABASE=absent
export PGUSER=lacannkj
export PGPASSWORD=112205401

psql < create.sql
./copy.sh
psql < alter.sql
psql < index.sql
psql < stats.sql
```