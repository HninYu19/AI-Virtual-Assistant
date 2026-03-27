import sqlite3

conn = sqlite3.connect('jarvis.db')
cursor = conn.cursor()

# Display current contacts before update
print("📋 Current contacts BEFORE update:")
cursor.execute('SELECT id, name, mobile_no, email FROM contacts')
current_contacts = cursor.fetchall()
for row in current_contacts:
    print(f"  ID: {row[0]} | Name: {row[1]} | Mobile: {row[2] or 'N/A'} | Email: {row[3]}")

# Add '+86' prefix to mobile numbers that don't already have it
# This will add '+86' to numbers that are not NULL and don't already start with '+86'
cursor.execute("""
    UPDATE contacts 
    SET mobile_no = '+86' || mobile_no
    WHERE mobile_no IS NOT NULL 
    AND mobile_no != '' 
    AND mobile_no NOT LIKE '+86%'
""")

# Commit the changes
conn.commit()

# Get count of updated records
cursor.execute("SELECT changes()")
updated_count = cursor.fetchone()[0]

print(f"\n✅ Updated {updated_count} records")

# Display updated contacts
print("\n📋 Updated contacts AFTER update:")
cursor.execute('SELECT id, name, mobile_no, email FROM contacts')
for row in cursor.fetchall():
    print(f"  ID: {row[0]} | Name: {row[1]} | Mobile: {row[2] or 'N/A'} | Email: {row[3]}")

# Close connection
conn.close()