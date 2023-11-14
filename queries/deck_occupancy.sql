---
--- Given a timestamp and a deck how many cars are parked in that deck
---

DROP FUNCTION IF EXISTS deck_occupancy(id integer, dt timestamp);

CREATE FUNCTION deck_occupancy(id integer, dt timestamp)
RETURNS TABLE(occupations bigint) AS $$

	SELECT SUM(o.occ)
	FROM decks as d
		JOIN observations AS o ON o.deck_id = d.deck_id
	WHERE 
		d.deck_id = id
	GROUP BY o.date_time
	order by abs(extract(epoch from (o.date_time - dt)))
	LIMIT 1
	
$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION deck_occupancy(id integer, dt timestamp) OWNER TO outliers;