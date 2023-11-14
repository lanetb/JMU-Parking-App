---
--- Given a date, time and day of the week, get the number of students in class in each building.
---

DROP FUNCTION IF EXISTS occupancy_date_time_each_building(date_v date, time_v time, day_v text);

CREATE FUNCTION occupancy_date_time_each_building(date_v date, time_v time, day_v text)
RETURNS TABLE(building_id integer, enrolled bigint) AS $$

    SELECT m.building_id, SUM(m.enrolled)
	FROM meetings AS m
		JOIN terms AS t ON m.term = t.term
	WHERE
		(
			t.start_date <= date_v
			AND t.end_date >= date_v
		)
		AND m.days LIKE day_v
		AND
		(
			m.start_t <= time_v
			AND m.end_t >= time_v
		)

	GROUP BY m.building_id
	ORDER BY m.building_id
    
$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION occupancy_date_time_each_building(date_v date, time_v time, day_v text) OWNER TO outliers;