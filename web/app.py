import os
import time
import datetime
import requests
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, session, redirect, url_for, Response
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'car-horizon-secret-key-12345')

# Fetch database configurations from environment variables
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'rootpassword')
DB_NAME = os.environ.get('DB_NAME', 'carhorizon')

# Static UI texts translation dictionary (English and French only)
UI_TRANSLATIONS = {
    # Brand
    "Car Horizon - Official Website": {"en": "Car Horizon - Official Website", "fr": "Car Horizon - Site Officiel"},
    "Models": {"en": "Models", "fr": "Modèles"},
    
    # Headers
    "Discover all models": {"en": "Discover all models", "fr": "Découvrir tous les modèles"},
    "Explore the entire range": {"en": "Explore the entire range", "fr": "Explorez toute la gamme"},
    "Exclusive offers": {"en": "Exclusive offers", "fr": "Offres exclusives"},
    "Default sorting": {"en": "Default sorting", "fr": "Tri par défaut"},
    "Price: Low to High": {"en": "Price: Low to High", "fr": "Prix : Du moins cher au plus cher"},
    "Price: High to Low": {"en": "Price: High to Low", "fr": "Prix : Du plus cher au moins cher"},
    "Color: A-Z": {"en": "Color: A-Z", "fr": "Couleur : A-Z"},
    "LEGENDARY HORIZONS": {"en": "LEGENDARY HORIZONS", "fr": "HORIZONS LÉGENDAIRES"},
    "Experience the ultimate collection of automotive masterpieces.": {
        "en": "Experience the ultimate collection of automotive masterpieces.",
        "fr": "Découvrez la collection ultime de chefs-d'œuvre automobiles."
    },
    "Explore Collection": {"en": "Explore Collection", "fr": "Explorer la collection"},
    
    # Filter Categories
    "Categories": {"en": "Categories", "fr": "Catégories"},
    "SUV": {"en": "SUV", "fr": "SUV"},
    "Estate": {"en": "Estate", "fr": "Break"},
    "Saloon": {"en": "Saloon", "fr": "Berline"},
    "Coupé": {"en": "Coupé", "fr": "Coupé"},
    "Compact": {"en": "Compact", "fr": "Compacte"},
    "Convertible": {"en": "Convertible", "fr": "Cabriolet"},
    
    # Capitalized categories dynamic matching
    "Suv": {"en": "SUV", "fr": "SUV"},
    "Break": {"en": "Estate", "fr": "Break"},
    "Berline": {"en": "Saloon", "fr": "Berline"},
    "Coupe": {"en": "Coupé", "fr": "Coupé"},
    "Compacte": {"en": "Compact", "fr": "Compacte"},
    "Cabriolet": {"en": "Convertible", "fr": "Cabriolet"},
    
    # Filter Series / Brands
    "Brands": {"en": "Brands", "fr": "Marques"},
    "All": {"en": "All", "fr": "Tous"},
    
    # Filter Motorisations
    "Engines": {"en": "Engines", "fr": "Motorisations"},
    "100% electric": {"en": "100% electric", "fr": "100 % électrique"},
    "Plug-in hybrid": {"en": "Plug-in hybrid", "fr": "Hybride rechargeable"},
    "Petrol": {"en": "Petrol", "fr": "Essence"},
    "Diesel": {"en": "Diesel", "fr": "Diesel"},

    # Card links & info
    "Do you like": {"en": "Do you like", "fr": "Aimez-vous"},
    "driving?": {"en": "driving?", "fr": "conduire?"},
    "Explore": {"en": "Explore", "fr": "Explorer"},
    "Download the full specifications": {"en": "Download the full specifications", "fr": "Télécharger la fiche technique complète"},
    
    # Footer UI
    "Legal notice": {"en": "Legal notice", "fr": "Mentions légales"},
    "Privacy policy": {"en": "Privacy policy", "fr": "Politique de confidentialité"},
    "View in 3D": {"en": "View in 3D", "fr": "Voir en 3D"},
    "Learn More": {"en": "Learn More", "fr": "En savoir plus"},
    "Back to models": {"en": "Back to models", "fr": "Retour aux modèles"},
    "Interactive 3D View": {"en": "Interactive 3D View", "fr": "Vue 3D Interactive"},
    "Engine Type": {"en": "Engine Type", "fr": "Type de moteur"},
    "Transmission": {"en": "Transmission", "fr": "Transmission"},
    "Top Speed": {"en": "Top Speed", "fr": "Vitesse maximale"},
    "Drivetrain": {"en": "Drivetrain", "fr": "Transmission (Roues)"},
    "Manual 6-Speed / Sequential": {"en": "Manual 6-Speed / Sequential", "fr": "Manuelle 6 rapports / Séquentielle"},
    "Automatic 8-Speed": {"en": "Automatic 8-Speed", "fr": "Automatique 8 rapports"},
    "LATEST NEWS": {"en": "Latest News", "fr": "Dernières Actualités"},
    "Call dealer for more information": {
        "en": "Call dealer for more information", 
        "fr": "Appeler le concessionnaire pour plus d'informations"
    },
    "Extended specifications": {"en": "Extended specifications", "fr": "Fiche technique détaillée"},
    
    # Specs Titles
    "Exterior Paint": {"en": "Exterior Paint", "fr": "Teinte extérieure"},
    "Wheels": {"en": "Wheels & Rims", "fr": "Jantes"},
    "Chassis Materials": {"en": "Chassis Materials", "fr": "Matériaux de construction"},
    "Dimensions & Wheelbase": {"en": "Dimensions & Wheelbase", "fr": "Empattement et Diamètre"},
    "Fuel Tank Capacity": {"en": "Fuel Tank Capacity", "fr": "Capacité du réservoir"},
    "Stopping Distance": {"en": "Stopping Distance", "fr": "Distance de freinage"},

    # Specs values
    "Renaissance Red / Absolute Zero White": {"en": "Renaissance Red / Absolute Zero White", "fr": "Rouge Renaissance / Blanc Absolute Zero"},
    "19-inch forged alloy wheels": {"en": "19-inch forged alloy wheels", "fr": "Jantes en alliage forgé 19 pouces"},
    "High-tensile steel and aluminum chassis": {"en": "High-tensile steel and aluminum chassis", "fr": "Châssis en acier haute résistance et aluminium"},
    "2,470 mm wheelbase": {"en": "2,470 mm wheelbase", "fr": "Empattement de 2 470 mm"},
    "52 Liters (13.7 gal)": {"en": "52 Liters (13.7 gal)", "fr": "52 Litres (13,7 gal)"},
    "31 meters (100-0 km/h)": {"en": "31 meters (100-0 km/h)", "fr": "31 mètres (100-0 km/h)"},
    "Bayside Blue Metallic": {"en": "Bayside Blue Metallic", "fr": "Bleu Métallisé Bayside"},
    "18-inch gold forged BBS wheels": {"en": "18-inch gold forged BBS wheels", "fr": "Jantes BBS forgées 18 pouces dorées"},
    "Steel and carbon hybrid chassis": {"en": "Steel and carbon hybrid chassis", "fr": "Châssis hybride acier et carbone"},
    "2,665 mm wheelbase": {"en": "2,665 mm wheelbase", "fr": "Empattement de 2 665 mm"},
    "65 Liters (17.2 gal)": {"en": "65 Liters (17.2 gal)", "fr": "65 Litres (17,2 gal)"},
    "33 meters (100-0 km/h)": {"en": "33 meters (100-0 km/h)", "fr": "33 mètres (100-0 km/h)"},
    "Matte Navy Blue Racing Livery": {"en": "Matte Navy Blue Racing Livery", "fr": "Livrée de course bleu marine mat"},
    "18-inch spec carbon racing wheels": {"en": "18-inch spec carbon racing wheels", "fr": "Jantes course en carbone de 18 pouces"},
    "Carbon fiber honeycomb monocoque": {"en": "Carbon fiber honeycomb monocoque", "fr": "Monocoque en nid d'abeille de fibre de carbone"},
    "3,600 mm wheelbase": {"en": "3,600 mm wheelbase", "fr": "Empattement de 3 600 mm"},
    "110 kg fuel capacity": {"en": "110 kg fuel capacity", "fr": "Capacité de carburant de 110 kg"},
    "25 meters (100-0 km/h)": {"en": "25 meters (100-0 km/h)", "fr": "25 mètres (100-0 km/h)"},
    "Brilliant Red / Jet Black Paint": {"en": "Brilliant Red / Jet Black Paint", "fr": "Rouge Brillant / Noir Intense"},
    "16-inch multi-spoke BBS wheels": {"en": "16-inch multi-spoke BBS wheels", "fr": "Jantes BBS multi-branches 16 pouces"},
    "Lightweight steel frame": {"en": "Lightweight steel frame", "fr": "Châssis en acier léger"},
    "2,565 mm wheelbase": {"en": "2,565 mm wheelbase", "fr": "Empattement de 2 565 mm"},
    "70 Liters (18.5 gal)": {"en": "70 Liters (18.5 gal)", "fr": "70 Litres (18,5 gal)"},
    "36 meters (100-0 km/h)": {"en": "36 meters (100-0 km/h)", "fr": "36 mètres (100-0 km/h)"},
    "Interlagos Blue Metallic": {"en": "Interlagos Blue Metallic", "fr": "Bleu Interlagos Métallisé"},
    "19-inch M double-spoke wheels": {"en": "19-inch M double-spoke wheels", "fr": "Jantes M à doubles rayons 19 pouces"},
    "Aluminum and steel hybrid structure": {"en": "Aluminum and steel hybrid structure", "fr": "Structure hybride aluminium et acier"},
    "2,889 mm wheelbase": {"en": "2,889 mm wheelbase", "fr": "Empattement de 2 889 mm"},
    "35 meters (100-0 km/h)": {"en": "35 meters (100-0 km/h)", "fr": "35 mètres (100-0 km/h)"},
    "Silver Arrow Metallic": {"en": "Silver Arrow Metallic", "fr": "Gris Métallisé Flèche d'Argent"},
    "15-inch steel wheels with chrome hubs": {"en": "15-inch steel wheels with chrome hubs", "fr": "Jantes acier 15 pouces avec moyeux chromés"},
    "Tubular spaceframe, aluminum panels": {"en": "Tubular spaceframe, aluminum panels", "fr": "Châssis tubulaire, panneaux en aluminium"},
    "2,400 mm wheelbase": {"en": "2,400 mm wheelbase", "fr": "Empattement de 2 400 mm"},
    "130 Liters (34.3 gal)": {"en": "130 Liters (34.3 gal)", "fr": "130 Litres (34,3 gal)"},
    "45 meters (100-0 km/h)": {"en": "45 meters (100-0 km/h)", "fr": "45 mètres (100-0 km/h)"},
    "Super Silver / Solid White Paint": {"en": "Super Silver / Solid White Paint", "fr": "Super Argent / Blanc Uni"},
    "20-inch RAYS lightweight wheels": {"en": "20-inch RAYS lightweight wheels", "fr": "Jantes ultra-légères RAYS 20 pouces"},
    "Carbon fiber body panels": {"en": "Carbon fiber body panels", "fr": "Panneaux de carrosserie en fibre de carbone"},
    "2,780 mm wheelbase": {"en": "2,780 mm wheelbase", "fr": "Empattement de 2 780 mm"},
    "74 Liters (19.5 gal)": {"en": "74 Liters (19.5 gal)", "fr": "74 Litres (19,5 gal)"},
    "30 meters (100-0 km/h)": {"en": "30 meters (100-0 km/h)", "fr": "30 mètres (100-0 km/h)"},
    "Guards Red / Grand Prix White": {"en": "Guards Red / Grand Prix White", "fr": "Rouge Guards / Blanc Grand Prix"},
    "16-inch Fuchs wheels": {"en": "16-inch Fuchs wheels", "fr": "Jantes Fuchs de 16 pouces"},
    "Galvanized steel body shell": {"en": "Galvanized steel body shell", "fr": "Carrosserie en acier galvanisé"},
    "2,272 mm wheelbase": {"en": "2,272 mm wheelbase", "fr": "Empattement de 2,272 mm"},
    "80 Liters (21.1 gal)": {"en": "80 Liters (21.1 gal)", "fr": "80 Litres (21,1 gal)"},
    "37 meters (100-0 km/h)": {"en": "37 meters (100-0 km/h)", "fr": "37 mètres (100-0 km/h)"},
    "Vintage Red / Brilliant Black": {"en": "Vintage Red / Brilliant Black", "fr": "Rouge Vintage / Noir Brillant"},
    "17-inch lightweight alloy wheels": {"en": "17-inch lightweight alloy wheels", "fr": "Jantes alliage léger de 17 pouces"},
    "Lightweight aluminum body structure": {"en": "Lightweight aluminum body structure", "fr": "Structure de carrosserie en aluminium léger"},
    "2,425 mm wheelbase": {"en": "2,425 mm wheelbase", "fr": "Empattement de 2 425 mm"},
    "76 Liters (20.1 gal)": {"en": "76 Liters (20.1 gal)", "fr": "76 Litres (20,1 gal)"},
    "34 meters (100-0 km/h)": {"en": "34 meters (100-0 km/h)", "fr": "34 mètres (100-0 km/h)"},
    "Rosso Corsa (Racing Red)": {"en": "Rosso Corsa (Racing Red)", "fr": "Rosso Corsa (Rouge Course)"},
    "17-inch Speedline split-rim wheels": {"en": "17-inch Speedline split-rim wheels", "fr": "Jantes démontables Speedline 17 pouces"},
    "Kevlar, carbon fiber & aluminum": {"en": "Kevlar, carbon fiber & aluminum panels", "fr": "Panneaux en Kevlar, fibre de carbone et aluminium"},
    "2,450 mm wheelbase": {"en": "2,450 mm wheelbase", "fr": "Empattement de 2 450 mm"},
    "120 Liters (31.7 gal)": {"en": "120 Liters (31.7 gal)", "fr": "120 Litres (31,7 gal)"},
    "32 meters (100-0 km/h)": {"en": "32 meters (100-0 km/h)", "fr": "32 mètres (100-0 km/h)"},

    # Admin Login translations
    "Admin Login": {"en": "Admin Login", "fr": "Connexion Admin"},
    "Username": {"en": "Username", "fr": "Nom d'utilisateur"},
    "Password": {"en": "Password", "fr": "Mot de passe"},
    "Log In": {"en": "Log In", "fr": "Se connecter"},
    "Logout": {"en": "Logout", "fr": "Déconnexion"},
    "Admin Dashboard": {"en": "Admin Dashboard", "fr": "Tableau de Bord Admin"},
    "Add New Model": {"en": "Add New Model", "fr": "Ajouter un Nouveau Modèle"},
    "Brand": {"en": "Brand", "fr": "Marque"},
    "Name": {"en": "Name", "fr": "Nom"},
    "Category": {"en": "Category", "fr": "Catégorie"},
    "Engine Type": {"en": "Engine Type", "fr": "Type de Moteur"},
    "Price (EN)": {"en": "Price (EN)", "fr": "Prix (EN)"},
    "Price (FR)": {"en": "Price (FR)", "fr": "Prix (FR)"},
    "Lease Info (EN)": {"en": "Lease Info (EN)", "fr": "Info Loyer (EN)"},
    "Lease Info (FR)": {"en": "Lease Info (FR)", "fr": "Info Loyer (FR)"},
    "Image Path": {"en": "Image Path", "fr": "Chemin de l'image"},
    "Exclusive Offer": {"en": "Exclusive Offer", "fr": "Offre Exclusive"},
    "Sketchfab ID": {"en": "Sketchfab ID", "fr": "ID Sketchfab"},
    "Add Car": {"en": "Add Car", "fr": "Ajouter la voiture"},
    "Invalid credentials": {"en": "Invalid credentials", "fr": "Identifiants invalides"},
    "Security & Monitoring": {"en": "Security & Monitoring", "fr": "Sécurité & Surveillance"},
    "Live Monitoring Console": {"en": "Live Monitoring Console", "fr": "Console de Surveillance en Direct"},
    "Live Feeds": {"en": "Live Feeds", "fr": "Flux en Direct"},
    "Back to Dashboard": {"en": "Back to Dashboard", "fr": "Retour au Tableau de Bord"},
    "Device Status": {"en": "Device Status", "fr": "Statut de l'appareil"},
    "System Logs": {"en": "System Logs", "fr": "Journaux Système"},
    "Simulate Events": {"en": "Simulate Events", "fr": "Simuler des Événements"},
    "Camera 1 (Entrance)": {"en": "Camera 1 (Entrance)", "fr": "Caméra 1 (Entrée)"},
    "Camera 2 (Garage)": {"en": "Camera 2 (Garage)", "fr": "Caméra 2 (Garage)"},
    "Thermal Arduino": {"en": "Thermal Arduino", "fr": "Arduino Thermique"},
}

def get_db_connection():
    """Attempt to connect to the database with retry logic."""
    retries = 10
    delay = 3
    connection = None
    for i in range(retries):
        try:
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if connection.is_connected():
                print(f"Successfully connected to the database after {i+1} attempts.")
                return connection
        except Error as e:
            print(f"Database connection attempt {i+1} failed: {e}")
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise e
    return connection

@app.before_request
def check_lang():
    # Handle language switches via query parameter
    lang_param = request.args.get('lang')
    if lang_param in ['en', 'fr']:
        session['lang'] = lang_param
    # Reset any unsupported language stored in session (e.g. old 'es' cookie)
    if session.get('lang') not in ['en', 'fr']:
        session['lang'] = 'en'

@app.context_processor
def inject_translations():
    lang = session.get('lang', 'en')
    def translate(key):
        translation = UI_TRANSLATIONS.get(key, {})
        return translation.get(lang, key)
    return dict(_=translate, current_lang=lang)

@app.route('/')
def index():
    connection = None
    cursor = None
    cars = []
    brands = []
    
    lang = session.get('lang', 'en')
    db_lang = lang if lang in ['en', 'fr'] else 'en'
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Query distinct brands
        cursor.execute("SELECT DISTINCT brand FROM cars ORDER BY brand")
        brands = [row['brand'] for row in cursor.fetchall()]
        
        # Query cars with language specific columns and join color spec
        query_cars = f"""
            SELECT c.id, c.brand, c.category, c.fuel_type, c.name, 
                   c.price_{db_lang} AS price, 
                   c.lease_info_{db_lang} AS lease_info, 
                   c.image_path, c.is_exclusive, c.sketchfab_id,
                   s.spec_value AS color
            FROM cars c
            LEFT JOIN car_specifications s ON c.id = s.car_id AND s.spec_title = 'Exterior Paint'
        """
        cursor.execute(query_cars)
        cars = cursor.fetchall()
        
    except Error as e:
        print(f"Error querying database: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    brands_with_logos = ['toyota', 'nissan', 'red bull', 'bmw', 'mercedes', 'porsche', 'ferrari', 'mazda']
    return render_template('index.html', cars=cars, brands=brands, brands_with_logos=brands_with_logos)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    connection = None
    cursor = None
    car = None
    extended_specs = []
    lang = session.get('lang', 'en')
    db_lang = lang if lang in ['en', 'fr'] else 'en'
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Query single car details with language specific columns
        query_car = f"""
            SELECT id, brand, category, fuel_type, name, 
                   price_{db_lang} AS price, 
                   lease_info_{db_lang} AS lease_info, 
                   image_path, is_exclusive, sketchfab_id 
            FROM cars
            WHERE id = %s
        """
        cursor.execute(query_car, (car_id,))
        car = cursor.fetchone()
        
        if car:
            # Query car specifications from SQL table
            query_specs = """
                SELECT spec_title AS title, spec_value AS value, spec_img AS img
                FROM car_specifications
                WHERE car_id = %s
            """
            cursor.execute(query_specs, (car_id,))
            extended_specs = cursor.fetchall()
        
    except Error as e:
        print(f"Error querying database for car detail: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
    if not car:
        return redirect(url_for('index'))
        
    return render_template('car_detail.html', car=car, extended_specs=extended_specs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        connection = None
        cursor = None
        admin = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
            admin = cursor.fetchone()
        except Error as e:
            print(f"Database error during login: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                
        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid credentials"
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    connection = None
    cursor = None
    cars = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, brand, name, category, fuel_type, price_en FROM cars ORDER BY id DESC")
        cars = cursor.fetchall()
    except Error as e:
        print(f"Database error in admin dashboard: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
    return render_template('admin.html', cars=cars)

@app.route('/admin/add-car', methods=['POST'])
def add_car():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    brand = request.form.get('brand')
    name = request.form.get('name')
    category = request.form.get('category')
    fuel_type = request.form.get('fuel_type')
    price_en = request.form.get('price_en')
    price_fr = request.form.get('price_fr')
    lease_info_en = request.form.get('lease_info_en', '')
    lease_info_fr = request.form.get('lease_info_fr', '')
    image_path = request.form.get('image_path', 'assets/supra.png')
    is_exclusive = 1 if request.form.get('is_exclusive') else 0
    sketchfab_id = request.form.get('sketchfab_id')
    if not sketchfab_id:
        sketchfab_id = None
        
    # Specs values
    spec_paint = request.form.get('spec_paint')
    spec_wheels = request.form.get('spec_wheels')
    spec_chassis = request.form.get('spec_chassis')
    spec_dimensions = request.form.get('spec_dimensions')
    spec_fuel = request.form.get('spec_fuel')
    spec_brakes = request.form.get('spec_brakes')
    
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Insert car
        query_car = """
            INSERT INTO cars (brand, category, fuel_type, name, price_en, price_fr, 
                              lease_info_en, lease_info_fr, image_path, is_exclusive, sketchfab_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_car, (brand, category, fuel_type, name, price_en, price_fr,
                                   lease_info_en, lease_info_fr, image_path, is_exclusive, sketchfab_id))
        car_id = cursor.lastrowid
        
        # Insert standard specs
        specs_to_insert = [
            (car_id, 'Exterior Paint', spec_paint, 'spec_paint.png'),
            (car_id, 'Wheels', spec_wheels, 'spec_wheel.png'),
            (car_id, 'Chassis Materials', spec_chassis, 'spec_material.png'),
            (car_id, 'Dimensions & Wheelbase', spec_dimensions, 'spec_dimensions.png'),
            (car_id, 'Fuel Tank Capacity', spec_fuel, 'spec_fuel.png'),
            (car_id, 'Stopping Distance', spec_brakes, 'spec_brakes.png')
        ]
        
        query_spec = """
            INSERT INTO car_specifications (car_id, spec_title, spec_value, spec_img)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(query_spec, specs_to_insert)
        
        connection.commit()
    except Error as e:
        print(f"Database error during adding car: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/monitoring')
def admin_monitoring():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    connection = None
    cursor = None
    logs = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, device_name, log_level, message, DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i:%s') as formatted_time FROM device_logs ORDER BY timestamp DESC LIMIT 50")
        logs = cursor.fetchall()
    except Error as e:
        print(f"Database error in admin monitoring: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
    return render_template('monitoring.html', logs=logs)

@app.route('/admin/live')
def admin_live():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    connection = None
    cursor = None
    latest_temp = "24.3"
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT message FROM device_logs WHERE device_name = 'Thermal Arduino' AND message LIKE '%°C%' ORDER BY timestamp DESC LIMIT 1")
        temp_log = cursor.fetchone()
        if temp_log:
            import re
            match = re.search(r'(\d+\.\d+)°C', temp_log['message'])
            if match:
                latest_temp = match.group(1)
    except Error as e:
        print(f"Database error in admin live: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
    return render_template('live.html', latest_temp=latest_temp)

@app.route('/admin/monitoring/simulate', methods=['POST'])
def simulate_log():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    device = request.form.get('device')
    level = request.form.get('level')
    message = request.form.get('message')
    
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO device_logs (device_name, log_level, message) VALUES (%s, %s, %s)",
            (device, level, message)
        )
        connection.commit()
    except Error as e:
        print(f"Database error during log simulation: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
    return redirect(url_for('admin_monitoring'))

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/video_feed/1')
def video_feed_1():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    try:
        req = requests.get('http://camera-service:5001/video_feed/1', stream=True, timeout=5)
        return Response(req.iter_content(chunk_size=1024), content_type=req.headers.get('Content-Type'))
    except Exception as e:
        print(f"Error proxying feed 1: {e}")
        return "Camera 1 unavailable", 503

@app.route('/video_feed/2')
def video_feed_2():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    try:
        req = requests.get('http://camera-service:5001/video_feed/2', stream=True, timeout=5)
        return Response(req.iter_content(chunk_size=1024), content_type=req.headers.get('Content-Type'))
    except Exception as e:
        print(f"Error proxying feed 2: {e}")
        return "Camera 2 unavailable", 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

