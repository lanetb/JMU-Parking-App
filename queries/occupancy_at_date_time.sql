---
--- Given a date and hour how many cars are parked in each deck?
---

DROP FUNCTION IF EXISTS occupancy_at_date_time(year integer, month integer, day integer, hour integer);

CREATE FUNCTION occupancy_at_date_time(year integer, month integer, day integer, hour integer)
RETURNS TABLE(deck text, occupations bigint, address text, latitude double precision, longitude double precision) AS $$

	SELECT d.deck_name, SUM(o.occ), d.address, d.latitude, d.longitude
	FROM decks as d
		JOIN observations AS o ON o.deck_id = d.deck_id
	WHERE 
		o.date_time >= CAST(CONCAT(year, '-', month, '-', day, ' ', hour, ':00:00') AS timestamp)
		AND date_time < CAST(CONCAT(year, '-', month, '-', day, ' ', hour + 1, ':00:00') AS timestamp)
	GROUP BY d.deck_id;
	
$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION occupancy_at_date_time(year integer, month integer, day integer, hour integer) OWNER TO outliers;