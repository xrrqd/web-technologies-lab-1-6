ALTER TABLE cars
ADD COLUMN dealer_id INTEGER,
ADD CONSTRAINT fk_dealer
FOREIGN KEY (dealer_id)
REFERENCES dealers(id)
ON DELETE SET NULL;


-- индекс для ускорения запросов
CREATE INDEX idx_cars_dealer ON cars(dealer_id);
