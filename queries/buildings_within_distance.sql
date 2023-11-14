---
--- Takes a deck name and a distance in miles and returns a table with all the 
--- buildings within that distance of the 
---

DROP FUNCTION IF EXISTS buildings_within_distance(deck text, dist real);

CREATE FUNCTION buildings_within_distance(deck text, dist real)
RETURNS TABLE(building_name text, distance real, minutes integer) AS $$

	SELECT b.building_name, di.distance, di.minutes
	FROM distances di
		JOIN buildings AS b on di.building_id = b.building_id
		JOIN decks AS d on di.deck_id = d.deck_id
	WHERE 
		d.deck_name = deck
		AND di.distance <= dist
	ORDER BY di.distance;
	
$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION buildings_within_distance(deck text, dist real) OWNER TO outliers;