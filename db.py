import sqlite3

conn = sqlite3.connect('hahaton.db')
cursor = conn.cursor()


def create_database():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commits (
            id INTEGER PRIMARY KEY, 
            date TEXT,
            person_id INTEGER,
            message TEXT)
    ''')
    conn.commit()


cursor.execute('SELECT message FROM commits')
rows = cursor.fetchall()
commits = []
for row in rows:
    commits.append(*row)


burnout_commits = ['FIX', 'STYLE']
for commit in commits:
    for bad_commit in burnout_commits:
        if bad_commit in commit:
            print(*bad_commit)

