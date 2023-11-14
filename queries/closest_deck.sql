---
--- Gets the closest parking deck to each building. Gives the distance in miles and minutes.
---

DROP FUNCTION IF EXISTS closest_deck();

CREATE FUNCTION closest_deck()
RETURNS TABLE(building_name text, building_latitude double precision, building_longitude double precision, building_address text, deck_id integer, minutes integer, distance real, building_id integer) AS $$

	SELECT DISTINCT b.building_name
		, b.latitude
		, b.longitude
		, b.address
		, FIRST_VALUE(d.deck_id) OVER (PARTITION BY b.building_name ORDER BY di.distance) AS deck_id
		, MIN(di.minutes) OVER (PARTITION BY b.building_name ORDER BY di.minutes) AS minutes
		, FIRST_VALUE(di.distance) OVER (PARTITION BY b.building_name ORDER BY di.minutes) AS distance
		, b.building_id
	FROM distances AS di
		JOIN buildings AS b ON di.building_id = b.building_id
		JOIN decks AS d ON di.deck_id = d.deck_id
	ORDER BY b.building_name
	
$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION closest_deck() OWNER TO outliers;