ALTER TABLE meetings ADD COLUMN meeting_id serial;
ALTER TABLE meetings ADD PRIMARY KEY (meeting_id);
ALTER TABLE distances ADD COLUMN distance_id serial;
ALTER TABLE distances ADD PRIMARY KEY (distance_id);
ALTER TABLE decks ADD COLUMN deck_id serial;
ALTER TABLE decks ADD PRIMARY KEY (deck_id);
ALTER TABLE buildings ADD COLUMN building_id serial;
ALTER TABLE buildings ADD PRIMARY KEY (building_id);
ALTER TABLE observations ADD COLUMN obs_id serial;
ALTER TABLE observations ADD PRIMARY KEY (obs_id);

ALTER TABLE meetings ADD FOREIGN KEY (building_id) References buildings;
ALTER TABLE meetings ADD FOREIGN KEY (term) References terms;
ALTER TABLE distances ADD FOREIGN KEY (building_id) References buildings;
ALTER TABLE distances ADD FOREIGN KEY (deck_id) References decks;
ALTER TABLE observations ADD FOREIGN KEY (deck_id) References decks;
