from flask import Blueprint, request, jsonify
from models import get_db, Shelf, Product

bp = Blueprint('recovery_controller', __name__)

@bp.route('/options', methods=['GET'])
def recovery_options():
    # return possible recovery choices
    return jsonify({'choices':['FORCE_IN','FORCE_OUT']})

@bp.route('/apply', methods=['POST'])
def apply_recovery():
    data = request.json
    slot = data.get('slot')
    action = data.get('action')
    if slot is None or action not in ('FORCE_IN','FORCE_OUT'):
        return jsonify({'error':'invalid input'}), 400
    db = get_db()
    shelf = db.query(Shelf).filter_by(slot=slot).first()
    if not shelf:
        return jsonify({'error':'slot not found'}), 404
    if action == 'FORCE_IN':
        sku = data.get('sku')
        prod = db.query(Product).filter_by(sku=sku).first()
        if not prod:
            return jsonify({'error':'product not registered'}), 400
        shelf.status = 'OCCUPIED'
        shelf.product_id = prod.id
        db.commit()
        return jsonify({'ok':True})
    else:
        shelf.status = 'EMPTY'
        shelf.product_id = None
        db.commit()
        return jsonify({'ok':True})
