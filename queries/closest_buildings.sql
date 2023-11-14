---
--- Takes a deck name and a number, and returns a table with the number closest buildings
--- to that deck along with their distance in miles and minutes.
---

DROP FUNCTION IF EXISTS closest_buildings(deck text, num_buildings integer);

CREATE FUNCTION closest_buildings(deck text, num_buildings integer)
RETURNS TABLE(building_name text, distance real, minutes integer) AS $$

	SELECT b.building_name, di.distance, di.minutes
	FROM distances AS di
		JOIN buildings AS b on di.building_id = b.building_id
		JOIN decks AS d on di.deck_id = d.deck_id
	WHERE d.deck_name = deck
	ORDER BY di.minutes
	LIMIT num_buildings;
	
$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION closest_buildings(deck text, num_buildings integer) OWNER TO outliers;
