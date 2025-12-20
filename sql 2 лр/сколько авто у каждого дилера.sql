SELECT dealer_id, COUNT(*) AS car_count
FROM cars
WHERE dealer_id IS NOT NULL
GROUP BY dealer_id
ORDER BY car_count DESC;
