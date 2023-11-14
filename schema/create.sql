--Creates Tables for Outliers
DROP TABLE IF EXISTS meetings;

CREATE TABLE meetings (
    course_nbr integer NOT NULL,
    term integer NOT NULL,
    days text NOT NULL,
    start_t time NOT NULL,
    end_t time NOT NULL,
    enrolled integer NOT NULL,
	building_id integer NOT NULL,
    meeting_id integer NOT NULL
);

ALTER TABLE meetings OWNER TO outliers;

COMMENT ON TABLE meetings IS 'JMU enrollment data';


DROP TABLE IF EXISTS observations;

CREATE TABLE observations (
    date_time timestamp NOT NULL,
    type text NOT NULL,
    occ integer NOT NULL,
	deck_id integer NOT NULL,
    obs_id integer NOT NULL
);

ALTER TABLE observations OWNER TO outliers;

COMMENT ON TABLE observations IS 'observation data for the parking decks';


DROP TABLE IF EXISTS distances;

CREATE TABLE distances (
    minutes integer NOT NULL,
    distance real NOT NULL,
	deck_id integer NOT NULL,
    building_id integer NOT NULL,
    distance_id integer NOT NULL
);

ALTER TABLE distances OWNER TO outliers;

COMMENT ON TABLE distances IS 'distance data for JMU buildings and parking decks';


DROP TABLE IF EXISTS decks;

CREATE TABLE decks (
    deck_name text NOT NULL,
    deck_id integer NOT NULL,
    address text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL
);

ALTER TABLE decks OWNER TO outliers;

COMMENT ON TABLE decks IS 'JMU parking decks';


DROP TABLE IF EXISTS buildings;


CREATE TABLE buildings (
    building_name text NOT NULL,
    building_id integer NOT NULL,
    address text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL
);

ALTER TABLE buildings OWNER TO outliers;

COMMENT ON TABLE buildings IS 'JMU buildings';


DROP TABLE IF EXISTS terms;

CREATE TABLE terms (
	term integer NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL
);

ALTER TABLE terms OWNER TO outliers;

COMMENT ON TABLE terms IS 'JMU terms with start and end dates';
