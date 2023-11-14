CREATE INDEX ON meetings (course_nbr, term, days, start_t, end_t, enrolled, building_id);
CREATE INDEX ON buildings (building_name);
CREATE INDEX ON distances (minutes, distance, deck_id, building_id);
CREATE INDEX ON decks (deck_name);
CREATE INDEX ON observations(date_time, type, occ, deck_id);