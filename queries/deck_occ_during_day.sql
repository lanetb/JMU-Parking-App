---
--- Given a date and deck show its occupancy through the day
---

---
--- Given a date and deck show its occupancy through the day
---

DROP FUNCTION IF EXISTS deck_occ_during_day(dt date, id text);

CREATE FUNCTION deck_occ_during_day(dt date, id text)

RETURNS TABLE(date_time text, occ int) AS $$

	SELECT to_char(date_time, 'HH24:MI'), occ
	FROM observations as o
	JOIN decks as d ON d.deck_id = o.deck_id
	WHERE 
        DATE(date_time) = dt
    AND
        deck_name = id
    AND
        type = 'Com'
    ORDER BY
        date_time;
	
$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION deck_occ_during_day(dt date, id text) OWNER TO outliers;