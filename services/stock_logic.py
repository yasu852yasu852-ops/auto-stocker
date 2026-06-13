from models import get_db, Shelf, Product, StockHistory
from sqlalchemy import asc
from datetime import datetime

class StockLogic:
    """1x8専用FIFO・空棚選定ロジック"""
    def __init__(self):
        self.db = get_db()

    def find_first_empty(self):
        return self.db.query(Shelf).filter(Shelf.status=='EMPTY').order_by(asc(Shelf.slot)).first()

    def find_fifo_product(self, sku):
        prod = self.db.query(Product).filter_by(sku=sku).first()
        if not prod:
            return None
        # find occupied shelves with that product ordered by stored_at asc
        shelf = self.db.query(Shelf).filter(Shelf.product_id==prod.id, Shelf.status=='OCCUPIED').order_by(asc(Shelf.stored_at)).first()
        return shelf

    def occupy_shelf(self, shelf: Shelf, product: Product):
        shelf.status = 'OCCUPIED'
        shelf.product_id = product.id
        shelf.stored_at = datetime.utcnow()
        self.db.add(StockHistory(shelf_id=shelf.id, product_id=product.id, action='IN'))
        self.db.commit()

    def release_shelf(self, shelf: Shelf):
        self.db.add(StockHistory(shelf_id=shelf.id, product_id=shelf.product_id, action='OUT'))
        shelf.status = 'EMPTY'
        shelf.product_id = None
        shelf.stored_at = None
        self.db.commit()

    def get_shelves(self):
        return self.db.query(Shelf).order_by(asc(Shelf.slot)).all()
