-- A script that lists bands with
-- a particular style and ranked
-- based on their longevity

SELECT band_name AS band_name,IFNULL(split, 2020) - IFNULL(formed, 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
