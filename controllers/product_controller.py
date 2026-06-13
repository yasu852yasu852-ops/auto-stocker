from flask import Blueprint, request, jsonify
from models import get_db, Product

bp = Blueprint('product_controller', __name__)

@bp.route('/', methods=['GET'])
def list_products():
    db = get_db()
    prods = db.query(Product).all()
    return jsonify([{'sku':p.sku, 'name':p.name} for p in prods])

@bp.route('/', methods=['POST'])
def create_product():
    data = request.json
    sku = data.get('sku')
    name = data.get('name')
    if not sku or not name:
        return jsonify({'error':'invalid input'}), 400
    db = get_db()
    if db.query(Product).filter_by(sku=sku).first():
        return jsonify({'error':'exists'}), 409
    p = Product(sku=sku, name=name)
    db.add(p)
    db.commit()
    return jsonify({'sku':p.sku, 'name':p.name}), 201

@bp.route('/<sku>', methods=['DELETE'])
def delete_product(sku):
    db = get_db()
    p = db.query(Product).filter_by(sku=sku).first()
    if not p:
        return jsonify({'error':'not found'}), 404
    db.delete(p)
    db.commit()
    return jsonify({'ok':True})
