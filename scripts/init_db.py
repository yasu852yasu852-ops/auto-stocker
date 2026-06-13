from models import init_db, get_db, Shelf

if __name__ == '__main__':
    init_db()
    db = get_db()
    # create 8 shelves if not present
    existing = db.query(Shelf).count()
    if existing == 0:
        for i in range(1,9):
            s = Shelf(slot=i, status='EMPTY')
            db.add(s)
        db.commit()
        print('Created 8 shelves')
    else:
        print('Shelves already exist')
