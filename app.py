from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database initialization
def init_db():
    with sqlite3.connect('database/goodhealthhub.db') as conn:
        cursor = conn.cursor()
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiry_date TEXT NOT NULL,
            donor_name TEXT
        );

        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camp_name TEXT NOT NULL,
            user_name TEXT NOT NULL,
            email TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            vaccine_name TEXT NOT NULL,
            dose_date TEXT NOT NULL
        );
                             
        CREATE TABLE IF NOT EXISTS health_tips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS symptoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptom_name TEXT NOT NULL,
    suggestions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    reminder_type TEXT NOT NULL,
    date_time TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS doctor_appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_name TEXT NOT NULL,
    user_name TEXT NOT NULL,
    appointment_date TEXT NOT NULL,
    contact TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fitness_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    fitness_goal TEXT NOT NULL,
    calories INT NOT NULL,
    progress TEXT
);

CREATE TABLE IF NOT EXISTS pharmacy_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT NOT NULL,
    pharmacy_name TEXT NOT NULL,
    location TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS mental_health_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_name TEXT NOT NULL,
    description TEXT NOT NULL,
    contact TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS donation_impact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_name TEXT NOT NULL,
    impact_details TEXT NOT NULL,
    beneficiaries INT NOT NULL
);

        ''')

        conn.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/medicine', methods=['GET', 'POST'])
def medicine():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        donor_name = request.form['donor_name']
        cursor.execute("INSERT INTO medicines (name, quantity, expiry_date, donor_name) VALUES (?, ?, ?, ?)", 
                       (name, quantity, expiry_date, donor_name))
        conn.commit()
        flash("Medicine added successfully!", "success")
        return redirect(url_for('medicine'))
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    conn.close()
    return render_template('medicine.html', medicines=medicines)

@app.route('/health_camp', methods=['GET', 'POST'])
def health_camp():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        camp_name = request.form['camp_name']
        user_name = request.form['user_name']
        email = request.form['email']
        cursor.execute("INSERT INTO registrations (camp_name, user_name, email) VALUES (?, ?, ?)",
                       (camp_name, user_name, email))
        conn.commit()
        flash("Registered successfully!", "success")
        return redirect(url_for('health_camp'))
    cursor.execute("SELECT * FROM registrations")
    registrations = cursor.fetchall()
    conn.close()
    return render_template('health_camp.html', registrations=registrations)

@app.route('/vaccination', methods=['GET', 'POST'])
def vaccination():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        user_name = request.form['user_name']
        vaccine_name = request.form['vaccine_name']
        dose_date = request.form['dose_date']
        cursor.execute("INSERT INTO vaccinations (user_name, vaccine_name, dose_date) VALUES (?, ?, ?)",
                       (user_name, vaccine_name, dose_date))
        conn.commit()
        flash("Vaccination record added successfully!", "success")
        return redirect(url_for('vaccination'))
    cursor.execute("SELECT * FROM vaccinations")
    vaccinations = cursor.fetchall()
    conn.close()
    return render_template('vaccination.html', vaccinations=vaccinations)

@app.route('/health_tips', methods=['GET', 'POST'])
def health_tips():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("INSERT INTO health_tips (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        flash("Health Tip added successfully!", "success")
    
    cursor.execute("SELECT * FROM health_tips ORDER BY created_at DESC")
    tips = cursor.fetchall()
    conn.close()
    return render_template('health_tips.html', tips=tips)

@app.route('/symptom_checker', methods=['GET', 'POST'])
def symptom_checker():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()

    suggestions = None
    if request.method == 'POST':
        symptom = request.form['symptom']
        cursor.execute("SELECT suggestions FROM symptoms WHERE symptom_name = ?", (symptom,))
        result = cursor.fetchone()
        suggestions = result[0] if result else "No suggestions found for this symptom."
    
    conn.close()
    return render_template('symptom_checker.html', suggestions=suggestions)

@app.route('/reminders', methods=['GET', 'POST'])
def reminders():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        user_name = request.form['user_name']
        reminder_type = request.form['reminder_type']
        date_time = request.form['date_time']
        cursor.execute("INSERT INTO reminders (user_name, reminder_type, date_time) VALUES (?, ?, ?)",
                       (user_name, reminder_type, date_time))
        conn.commit()
        flash("Reminder added successfully!", "success")
    
    cursor.execute("SELECT * FROM reminders ORDER BY date_time ASC")
    reminders = cursor.fetchall()
    conn.close()
    return render_template('reminders.html', reminders=reminders)

@app.route('/doctor_consultation', methods=['GET', 'POST'])
def doctor_consultation():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        doctor_name = request.form['doctor_name']
        user_name = request.form['user_name']
        appointment_date = request.form['appointment_date']
        contact = request.form['contact']
        cursor.execute("INSERT INTO doctor_appointments (doctor_name, user_name, appointment_date, contact) VALUES (?, ?, ?, ?)",
                       (doctor_name, user_name, appointment_date, contact))
        conn.commit()
        flash("Appointment booked successfully!", "success")
    
    cursor.execute("SELECT * FROM doctor_appointments ORDER BY appointment_date ASC")
    appointments = cursor.fetchall()
    conn.close()
    return render_template('doctor_consultation.html', appointments=appointments)

@app.route('/fitness_tracker', methods=['GET', 'POST'])
def fitness_tracker():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        user_name = request.form['user_name']
        fitness_goal = request.form['fitness_goal']
        calories = request.form['calories']
        progress = request.form['progress']
        cursor.execute("INSERT INTO fitness_logs (user_name, fitness_goal, calories, progress) VALUES (?, ?, ?, ?)",
                       (user_name, fitness_goal, calories, progress))
        conn.commit()
        flash("Fitness log added successfully!", "success")
    
    cursor.execute("SELECT * FROM fitness_logs ORDER BY id DESC")
    logs = cursor.fetchall()
    conn.close()
    return render_template('fitness_tracker.html', logs=logs)

@app.route('/pharmacy', methods=['GET', 'POST'])
def pharmacy():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        medicine_name = request.form['medicine_name']
        pharmacy_name = request.form['pharmacy_name']
        location = request.form['location']
        price = request.form['price']
        cursor.execute("INSERT INTO pharmacy_inventory (medicine_name, pharmacy_name, location, price) VALUES (?, ?, ?, ?)",
                       (medicine_name, pharmacy_name, location, price))
        conn.commit()
        flash("Pharmacy inventory updated!", "success")
    
    cursor.execute("SELECT * FROM pharmacy_inventory")
    inventory = cursor.fetchall()
    conn.close()
    return render_template('pharmacy.html', inventory=inventory)

@app.route('/mental_health', methods=['GET', 'POST'])
def mental_health():
    conn = sqlite3.connect('database/goodhealthhub.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        resource_name = request.form['resource_name']
        description = request.form['description']
        contact = request.form['contact']
        cursor.execute("INSERT INTO mental_health_resources (resource_name, description, contact) VALUES (?, ?, ?)",
                       (resource_name, description, contact))
        conn.commit()
        flash("Mental Health Resource added!", "success")
    
    cursor.execute("SELECT * FROM mental_health_resources")
    resources = cursor.fetchall()
    conn.close()
    return render_template('mental_health.html', resources=resources)



if __name__ == '__main__':
    init_db()
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
 
