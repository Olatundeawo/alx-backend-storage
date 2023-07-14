-- A script that rannks country ordered by the
-- number of fans

SELECT origin AS origin, SUM(fan) AS nb_fans FROM
metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;