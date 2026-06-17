CREATE DATABASE IF NOT EXISTS carhorizon;
USE carhorizon;

DROP TABLE IF EXISTS car_specifications;
DROP TABLE IF EXISTS cars;
CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    price_en VARCHAR(50) NOT NULL,
    price_fr VARCHAR(50) NOT NULL,
    lease_info_en VARCHAR(255) DEFAULT '',
    lease_info_fr VARCHAR(255) DEFAULT '',
    image_path VARCHAR(255) NOT NULL,
    is_exclusive BOOLEAN DEFAULT FALSE,
    sketchfab_id VARCHAR(100) DEFAULT NULL
);

DROP TABLE IF EXISTS admins;
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Seed cars (10 iconic cars list)
INSERT INTO cars (
    id, brand, category, fuel_type, name, 
    price_en, price_fr, 
    lease_info_en, lease_info_fr, 
    image_path, is_exclusive,
    sketchfab_id
) VALUES
(
    1, 'Toyota', 'coupe', 'petrol', 'Supra MK4 (A80)',
    '$650/month', '650 €/mois',
    'Classic sports lease, 36 mos.', 'Loyer sportif classique, 36 mois.',
    'assets/supra.png', 1,
    '61d402d6de904374bfe5a98907c85b1d'
),
(
    2, 'Nissan', 'coupe', 'petrol', 'Skyline GT-R (R34 V-Spec II)',
    '$890/month', '890 €/mois',
    'JDM collector lease, 36 mos.', 'Loyer JDM collector, 36 mois.',
    'assets/skyline.png', 1,
    '778a13fa476c4806b9df75a87a6ecf7c'
),
(
    3, 'Red Bull', 'coupe', 'petrol', 'Oracle Red Bull Racing RB19',
    '$25,000/day', '25 000 €/jour',
    'Track experience only.', 'Expérience sur piste uniquement.',
    'assets/rb19.png', 1,
    '40f21cd4a660427dbd6caa797bec4c72'
),
(
    4, 'BMW', 'coupe', 'petrol', 'M3 (E30 Sport Evolution)',
    '$720/month', '720 €/mois',
    'Classic legend lease, 36 mos.', 'Loyer légende classique, 36 mois.',
    'assets/m3_e30.png', 0,
    '9099df483850404a8cf94529b3df148b'
),
(
    5, 'BMW', 'berline', 'petrol', 'M5 (E60 V10)',
    '$590/month', '590 €/mois',
    'V10 performance lease, 36 mos.', 'Loyer performance V10, 36 mois.',
    'assets/m5_e60.png', 0,
    '4ebe7de65edf40d6b2b0c91cf41f17f3'
),
(
    6, 'Mercedes', 'coupe', 'petrol', '300 SL Gullwing',
    '$2,100/month', '2 100 €/mois',
    'Heritage collector lease, 48 mos.', 'Loyer héritage collection, 48 mois.',
    'assets/gullwing.png', 0,
    '68204ea507a240cb88763d9c75f2822e'
),
(
    7, 'Nissan', 'coupe', 'petrol', 'GT-R Nismo (R35)',
    '$1,250/month', '1 250 €/mois',
    'Nismo track lease, 36 mos.', 'Loyer Nismo piste, 36 mois.',
    'assets/gtr_r35.png', 0,
    '14885ab9272146218e051f52f796ed7d'
),
(
    8, 'Porsche', 'coupe', 'petrol', '911 Turbo (930)',
    '$980/month', '980 €/mois',
    'Vintage air-cooled lease, 36 mos.', 'Loyer vintage refroidi par air, 36 mois.',
    'assets/porsche_930.png', 0,
    '4e5d17a024a148cdb244b5d88d347a78'
),
(
    9, 'Mazda', 'coupe', 'petrol', 'RX-7 (FD3S)',
    '$550/month', '550 €/mois',
    'Rotary engine lease, 36 mos.', 'Loyer moteur rotatif, 36 mois.',
    'assets/rx7_fd.png', 0,
    'da181d6e901e459182bc7754925ed50f'
),
(
    10, 'Ferrari', 'coupe', 'petrol', 'F40',
    '$4,500/month', '4 500 €/mois',
    'Hypercar collector lease, 48 mos.', 'Loyer collection hypercar, 48 mois.',
    'assets/f40.png', 0,
    '52a66c41cfcd4f999fb1b1c49bf24d70'
);

-- Seed admins (admin / progtr00)
INSERT INTO admins (username, password_hash) VALUES
('admin', 'scrypt:32768:8:1$4R4HdNWT81HPqMaf$5012a993e841386966bc0ed860276f534ff282239c32ebcaec913ef03b1c575c4cffb4b121ad69e26348b68d0dcd67ffec3b3aff02acd28b339a76709776351a');

-- Create car_specifications table
CREATE TABLE car_specifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT NOT NULL,
    spec_title VARCHAR(100) NOT NULL,
    spec_value VARCHAR(255) NOT NULL,
    spec_img VARCHAR(100) NOT NULL,
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
);

-- Seed car_specifications
INSERT INTO car_specifications (car_id, spec_title, spec_value, spec_img) VALUES
-- Supra (ID: 1)
(1, 'Exterior Paint', 'Renaissance Red / Absolute Zero White', 'spec_paint.png'),
(1, 'Wheels', '19-inch forged alloy wheels', 'spec_wheel.png'),
(1, 'Chassis Materials', 'High-tensile steel and aluminum chassis', 'spec_material.png'),
(1, 'Dimensions & Wheelbase', '2,470 mm wheelbase', 'spec_dimensions.png'),
(1, 'Fuel Tank Capacity', '52 Liters (13.7 gal)', 'spec_fuel.png'),
(1, 'Stopping Distance', '31 meters (100-0 km/h)', 'spec_brakes.png'),

-- Skyline (ID: 2)
(2, 'Exterior Paint', 'Bayside Blue Metallic', 'spec_paint.png'),
(2, 'Wheels', '18-inch gold forged BBS wheels', 'spec_wheel.png'),
(2, 'Chassis Materials', 'Steel and carbon hybrid chassis', 'spec_material.png'),
(2, 'Dimensions & Wheelbase', '2,665 mm wheelbase', 'spec_dimensions.png'),
(2, 'Fuel Tank Capacity', '65 Liters (17.2 gal)', 'spec_fuel.png'),
(2, 'Stopping Distance', '33 meters (100-0 km/h)', 'spec_brakes.png'),

-- RB19 (ID: 3)
(3, 'Exterior Paint', 'Matte Navy Blue Racing Livery', 'spec_paint.png'),
(3, 'Wheels', '18-inch spec carbon racing wheels', 'spec_wheel.png'),
(3, 'Chassis Materials', 'Carbon fiber honeycomb monocoque', 'spec_material.png'),
(3, 'Dimensions & Wheelbase', '3,600 mm wheelbase', 'spec_dimensions.png'),
(3, 'Fuel Tank Capacity', '110 kg fuel capacity', 'spec_fuel.png'),
(3, 'Stopping Distance', '25 meters (100-0 km/h)', 'spec_brakes.png'),

-- M3 E30 (ID: 4)
(4, 'Exterior Paint', 'Brilliant Red / Jet Black Paint', 'spec_paint.png'),
(4, 'Wheels', '16-inch multi-spoke BBS wheels', 'spec_wheel.png'),
(4, 'Chassis Materials', 'Lightweight steel frame', 'spec_material.png'),
(4, 'Dimensions & Wheelbase', '2,565 mm wheelbase', 'spec_dimensions.png'),
(4, 'Fuel Tank Capacity', '70 Liters (18.5 gal)', 'spec_fuel.png'),
(4, 'Stopping Distance', '36 meters (100-0 km/h)', 'spec_brakes.png'),

-- M5 E60 (ID: 5)
(5, 'Exterior Paint', 'Interlagos Blue Metallic', 'spec_paint.png'),
(5, 'Wheels', '19-inch M double-spoke wheels', 'spec_wheel.png'),
(5, 'Chassis Materials', 'Aluminum and steel hybrid structure', 'spec_material.png'),
(5, 'Dimensions & Wheelbase', '2,889 mm wheelbase', 'spec_dimensions.png'),
(5, 'Fuel Tank Capacity', '70 Liters (18.5 gal)', 'spec_fuel.png'),
(5, 'Stopping Distance', '35 meters (100-0 km/h)', 'spec_brakes.png'),

-- 300 SL (ID: 6)
(6, 'Exterior Paint', 'Silver Arrow Metallic', 'spec_paint.png'),
(6, 'Wheels', '15-inch steel wheels with chrome hubs', 'spec_wheel.png'),
(6, 'Chassis Materials', 'Tubular spaceframe, aluminum panels', 'spec_material.png'),
(6, 'Dimensions & Wheelbase', '2,400 mm wheelbase', 'spec_dimensions.png'),
(6, 'Fuel Tank Capacity', '130 Liters (34.3 gal)', 'spec_fuel.png'),
(6, 'Stopping Distance', '45 meters (100-0 km/h)', 'spec_brakes.png'),

-- GT-R R35 (ID: 7)
(7, 'Exterior Paint', 'Super Silver / Solid White Paint', 'spec_paint.png'),
(7, 'Wheels', '20-inch RAYS lightweight wheels', 'spec_wheel.png'),
(7, 'Chassis Materials', 'Carbon fiber body panels', 'spec_material.png'),
(7, 'Dimensions & Wheelbase', '2,780 mm wheelbase', 'spec_dimensions.png'),
(7, 'Fuel Tank Capacity', '74 Liters (19.5 gal)', 'spec_fuel.png'),
(7, 'Stopping Distance', '30 meters (100-0 km/h)', 'spec_brakes.png'),

-- Porsche 930 (ID: 8)
(8, 'Exterior Paint', 'Guards Red / Grand Prix White', 'spec_paint.png'),
(8, 'Wheels', '16-inch Fuchs wheels', 'spec_wheel.png'),
(8, 'Chassis Materials', 'Galvanized steel body shell', 'spec_material.png'),
(8, 'Dimensions & Wheelbase', '2,272 mm wheelbase', 'spec_dimensions.png'),
(8, 'Fuel Tank Capacity', '80 Liters (21.1 gal)', 'spec_fuel.png'),
(8, 'Stopping Distance', '37 meters (100-0 km/h)', 'spec_brakes.png'),

-- RX-7 FD (ID: 9)
(9, 'Exterior Paint', 'Vintage Red / Brilliant Black', 'spec_paint.png'),
(9, 'Wheels', '17-inch lightweight alloy wheels', 'spec_wheel.png'),
(9, 'Chassis Materials', 'Lightweight aluminum body structure', 'spec_material.png'),
(9, 'Dimensions & Wheelbase', '2,425 mm wheelbase', 'spec_dimensions.png'),
(9, 'Fuel Tank Capacity', '76 Liters (20.1 gal)', 'spec_fuel.png'),
(9, 'Stopping Distance', '34 meters (100-0 km/h)', 'spec_brakes.png'),

-- Ferrari F40 (ID: 10)
(10, 'Exterior Paint', 'Rosso Corsa (Racing Red)', 'spec_paint.png'),
(10, 'Wheels', '17-inch Speedline split-rim wheels', 'spec_wheel.png'),
(10, 'Chassis Materials', 'Kevlar, carbon fiber & aluminum', 'spec_material.png'),
(10, 'Dimensions & Wheelbase', '2,450 mm wheelbase', 'spec_dimensions.png'),
(10, 'Fuel Tank Capacity', '120 Liters (31.7 gal)', 'spec_fuel.png'),
(10, 'Stopping Distance', '32 meters (100-0 km/h)', 'spec_brakes.png');

-- Create device_logs table for camera and thermal sensor tracking
DROP TABLE IF EXISTS device_logs;
CREATE TABLE device_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_name VARCHAR(50) NOT NULL,
    log_level VARCHAR(20) NOT NULL,
    message VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed device_logs with recent realistic timestamps
INSERT INTO device_logs (device_name, log_level, message, timestamp) VALUES
('Camera 1 (Entrance)', 'INFO', 'System startup - Camera stream initialized.', NOW() - INTERVAL 60 MINUTE),
('Camera 2 (Garage)', 'INFO', 'System startup - Camera stream initialized.', NOW() - INTERVAL 55 MINUTE),
('Thermal Arduino', 'INFO', 'Thermal sensor calibrated. Baseline temperature: 21.5°C.', NOW() - INTERVAL 50 MINUTE),
('Camera 1 (Entrance)', 'INFO', 'Motion detected - Person entering building.', NOW() - INTERVAL 40 MINUTE),
('Camera 2 (Garage)', 'INFO', 'Motion detected - BMW M3 E30 light sensor triggered.', NOW() - INTERVAL 30 MINUTE),
('Thermal Arduino', 'WARNING', 'High temperature warning - 38.2°C detected in Engine Bay A.', NOW() - INTERVAL 20 MINUTE),
('Thermal Arduino', 'ALERT', 'CRITICAL HEAT SPIKE - 58.7°C detected! Cooling fan activated.', NOW() - INTERVAL 15 MINUTE),
('Camera 1 (Entrance)', 'INFO', 'Unknown vehicle approaching gate.', NOW() - INTERVAL 10 MINUTE),
('Thermal Arduino', 'INFO', 'Temperature stabilized to 24.3°C.', NOW() - INTERVAL 5 MINUTE);
