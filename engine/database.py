import sqlite3

conn = sqlite3.connect('jarvis.db')
cursor = conn.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id INTEGER PRIMARY KEY, name VARCHAR(255), path VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null, 'WPS Office', 'C:\\Users\\User\\AppData\\Local\\Kingsoft\\WPS Office\\ksolaunch.exe')"
#cursor.execute(query)
#conn.commit()

#query = "CREATE TABLE IF NOT EXISTS web_command(id INTEGER PRIMARY KEY, name VARCHAR(255), url VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO web_command VALUES (null, 'gmail', 'https://www.gmail.com/')"
#cursor.execute(query)
#conn.commit()

#def import_contacts():
#    """Import contacts from CSV to SQLite database"""
    
    # Get paths
#    script_dir = os.path.dirname(os.path.abspath(__file__))
#    csv_path = os.path.join(os.path.dirname(script_dir), 'contacts.csv')
#    db_path = os.path.join(script_dir, 'jarvis.db')
    
#    print(f"Importing from: {csv_path}")
    
    # Recreate table with proper structure (mobile_no can be NULL)
#    cursor.execute('DROP TABLE IF EXISTS contacts')
#    cursor.execute('''CREATE TABLE contacts (id INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR(200),mobile_no VARCHAR(255),email VARCHAR(255))''')
    
    # Import CSV data
#    with open(csv_path, 'r', encoding='utf-8') as csvfile:csvreader = csv.reader(csvfile)
        
        # Skip header
#        next(csvreader)
        
#        count = 0
#        for row in csvreader:
#            if len(row) > 18:  # Ensure we have enough columns
                # Combine first and last name if available
#                first_name = row[0].strip() if len(row) > 0 else ''
#                last_name = row[2].strip() if len(row) > 2 else ''
#                name = f"{first_name} {last_name}".strip() if last_name else first_name
                
                # Get email
#                email = row[18].strip() if len(row) > 18 else ''
                
                # Only insert if we have at least a name
#                if name:
#                   cursor.execute(
#                        'INSERT INTO contacts (name, mobile_no, email) VALUES (?, ?, ?)',
#                        (name, None, email)  # mobile_no set to NULL since no phone numbers
#                    )
#                    count += 1
#                    print(f"Imported: {name} | Email: {email}")
        
#        print(f"\n✅ Imported {count} contacts")
    
    # Commit and close
#    conn.commit()
#    conn.close()
    
    # Verify
#    verify_contacts(db_path)

#def verify_contacts(db_path):
#    """Verify imported data"""
#    conn = sqlite3.connect(db_path)
#    cursor = conn.cursor()
    
#    print("\n📋 Database contents:")
#    cursor.execute('SELECT id, name, mobile_no, email FROM contacts LIMIT 10')
#    for row in cursor.fetchall():
#        print(f"  ID: {row[0]} | Name: {row[1]} | Mobile: {row[2] or 'N/A'} | Email: {row[3]}")
    
#    cursor.execute('SELECT COUNT(*) FROM contacts')
#    total = cursor.fetchone()[0]
#    print(f"\nTotal contacts: {total}")
    
#    conn.close()

#if __name__ == "__main__":
#    import_contacts()