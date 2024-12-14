import sqlite3

def initialize_db():
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    
    # Create table for parking slots
    c.execute('''
        CREATE TABLE IF NOT EXISTS parking_slots (
            slot_id INTEGER PRIMARY KEY,
            plate TEXT,
            entry_time TEXT,
            occupied BOOLEAN
        )
    ''')
    
    # Create table for parking records
    c.execute('''
        CREATE TABLE IF NOT EXISTS parking_records (
            record_id INTEGER PRIMARY KEY,
            plate TEXT,
            entry_time TEXT,
            exit_time TEXT,
            fee REAL
        )
    ''')
    
    # Initialize slots (if they don't already exist)
    for i in range(1, 31):
        c.execute('INSERT OR IGNORE INTO parking_slots (slot_id, occupied) VALUES (?, ?)', (i, False))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
