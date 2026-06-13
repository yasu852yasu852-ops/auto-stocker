import os
from models import get_db, StockHistory
import csv
from datetime import datetime

LOG_DIR = '/opt/auto-stocker/logs'
ARCHIVE_DIR = os.path.join(LOG_DIR, 'archives')

os.makedirs(ARCHIVE_DIR, exist_ok=True)

def rotate_monthly():
    db = get_db()
    # export previous month data
    now = datetime.utcnow()
    filename = os.path.join(ARCHIVE_DIR, f'stock_history_{now.year}_{now.month}.csv')
    rows = db.query(StockHistory).all()
    if not rows:
        return
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id','shelf_id','product_id','action','timestamp'])
        for r in rows:
            writer.writerow([r.id, r.shelf_id, r.product_id, r.action, r.timestamp])
    # Optionally truncate table - skipped here (manual operation)
    return filename

if __name__ == '__main__':
    print('rotate ->', rotate_monthly())
