---
--- Given a term, day, and time how many people will be in the building?
---

DROP FUNCTION IF EXISTS occupancy_term_day_time_building(incterm integer, day text, startt time without time zone, endt time without time zone);

CREATE FUNCTION occupancy_term_day_time_building(incterm integer, day text, startt time without time zone, endt time without time zone)
RETURNS TABLE(building text, enrolled bigint) AS $$

    SELECT b.building_name, SUM(m.enrolled)
    FROM buildings as b
        JOIN meetings AS m ON b.building_id = m.building_id
    WHERE 
        m.days LIKE CONCAT('%', day, '%') 
    AND ((m.end_t > startt AND m.end_t < endt) OR (m.start_t < endt AND m.start_t > startt) OR startt = m.start_t) 
    AND incterm = term
    GROUP BY b.building_id;
    
$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION occupancy_term_day_time_building(incterm integer, day text, startt time without time zone, endt time without time zone) OWNER TO outliers;