from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def initialize_database():
    conn = sqlite3.connect('cafe.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       table_number INTEGER,
                       item_name TEXT,
                       item_price REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS archived_bills
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       table_number INTEGER,
                       total_amount REAL)''')
    conn.commit()
    conn.close()

# Initialize database
initialize_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    table_number = request.form['table_number']
    item_name = request.form['item_name']
    item_price = request.form['item_price']

    conn = sqlite3.connect('cafe.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO orders (table_number, item_name, item_price)
                      VALUES (?, ?, ?)''', (table_number, item_name, item_price))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/pay_bill/<int:table_number>')
def pay_bill(table_number):
    conn = sqlite3.connect('cafe.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT item_name, item_price FROM orders WHERE table_number=?''', (table_number,))
    orders = cursor.fetchall()

    total_amount = sum(order[1] for order in orders)

    cursor.execute('''INSERT INTO archived_bills (table_number, total_amount)
                      VALUES (?, ?)''', (table_number, total_amount))

    cursor.execute('''DELETE FROM orders WHERE table_number=?''', (table_number,))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
