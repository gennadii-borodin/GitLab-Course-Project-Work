def get_all_things(db):
    cursor = db.execute('SELECT * from things')
    rows = cursor.fetchall()
    things = []
    if rows and len(rows) > 0:
        for row in rows:
            things.append(dict(row))
    return things