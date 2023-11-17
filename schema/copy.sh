#!/bin/sh
#
# NOTE: \copy imports from a local file
#       COPY imports from another database

echo \copy decks FROM csv
psql -c "\copy decks FROM decks.csv WITH CSV HEADER" absent

echo \copy building FROM csv
psql -c "\copy buildings FROM buildings.csv WITH CSV HEADER" absent

echo \copy class FROM csv
psql -c "\copy meetings FROM meetings.csv WITH CSV HEADER" absent

echo \copy opservations FROM csv
psql -c "\copy observations FROM observations.csv WITH CSV HEADER" absent

echo \copy distance FROM csv
psql -c "\copy distances FROM distances.csv WITH CSV HEADER" absent

echo \copy terms FROM csv
psql -c "\copy terms FROM terms.csv WITH CSV HEADER" absent

