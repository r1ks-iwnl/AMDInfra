-- All runs sorted by date descending
SELECT * FROM runs
ORDER BY run_date DESC;

--Coverpoint coverage for given run_id
SELECT coverage from coverpoints
WHERE run_id = 1;

--How many MISS bins in a run
SELECT COUNT(*) AS miss_bins
FROM runs r
JOIN coverpoints c ON c.run_id = r.id
JOIN bins b ON c.id = b.coverpoint_id
WHERE r.id = 1 AND b.hit = 0;

--How many bins in a run
SELECT COUNT(bins.id) AS total_bins
FROM bins
JOIN coverpoints ON bins.coverpoint_id = coverpoints.id
WHERE coverpoints.run_id = 1; 