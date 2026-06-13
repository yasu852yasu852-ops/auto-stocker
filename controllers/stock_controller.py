from flask import Blueprint, request, jsonify
from services.stock_logic import StockLogic
from models import get_db, Product, Shelf
from utils.serial_ctrl import serial_ctrl
from services.system_lock import acquire, release, is_busy

bp = Blueprint('stock_controller', __name__)
logic = StockLogic()

@bp.route('/state', methods=['GET'])
def state():
    shelves = logic.get_shelves()
    out = []
    for s in shelves:
        out.append({'slot':s.slot, 'status':s.status, 'product': s.product.sku if s.product else None, 'stored_at': s.stored_at})
    return jsonify(out)

@bp.route('/in/auto', methods=['POST'])
def inbound_auto():
    data = request.json
    sku = data.get('sku')
    if not sku:
        return jsonify({'error':'sku required'}), 400
    db = get_db()
    product = db.query(Product).filter_by(sku=sku).first()
    if not product:
        return jsonify({'error':'product not registered'}), 400
    # check lock
    if not acquire():
        return jsonify({'error':'system busy'}), 423
    shelf = logic.find_first_empty()
    if not shelf:
        release()
        return jsonify({'error':'no empty shelf', 'code':'ERR-101'}), 409
    # send to device
    serial_ctrl.connect()
    serial_ctrl.send(f'IN {shelf.slot} {sku}')
    logic.occupy_shelf(shelf, product)
    # release lock (clients see busy for TIMEOUT seconds)
    release()
    return jsonify({'ok':True, 'slot':shelf.slot})

@bp.route('/out/auto', methods=['POST'])
def outbound_auto():
    data = request.json
    sku = data.get('sku')
    if not sku:
        return jsonify({'error':'sku required'}), 400
    if not acquire():
        return jsonify({'error':'system busy'}), 423
    shelf = logic.find_fifo_product(sku)
    if not shelf:
        release()
        return jsonify({'error':'product not found', 'code':'ERR-102'}), 404
    serial_ctrl.connect()
    serial_ctrl.send(f'OUT {shelf.slot} {sku}')
    logic.release_shelf(shelf)
    release()
    return jsonify({'ok':True, 'slot':shelf.slot})

@bp.route('/in/manual', methods=['POST'])
def inbound_manual():
    data = request.json
    slot = data.get('slot')
    sku = data.get('sku')
    if slot is None or sku is None:
        return jsonify({'error':'slot and sku required'}), 400
    db = get_db()
    product = db.query(Product).filter_by(sku=sku).first()
    if not product:
        return jsonify({'error':'product not registered'}), 400
    shelf = db.query(Shelf).filter_by(slot=slot).first()
    if not shelf:
        return jsonify({'error':'slot not found'}), 404
    if shelf.status == 'OCCUPIED':
        return jsonify({'error':'slot occupied'}), 409
    if not acquire():
        return jsonify({'error':'system busy'}), 423
    serial_ctrl.connect()
    serial_ctrl.send(f'IN {shelf.slot} {sku}')
    logic.occupy_shelf(shelf, product)
    release()
    return jsonify({'ok':True, 'slot':shelf.slot})

@bp.route('/out/manual', methods=['POST'])
def outbound_manual():
    data = request.json
    slot = data.get('slot')
    if slot is None:
        return jsonify({'error':'slot required'}), 400
    db = get_db()
    s = db.query(Shelf).filter_by(slot=slot).first()
    if not s:
        return jsonify({'error':'slot not found'}), 404
    if s.status == 'EMPTY':
        return jsonify({'error':'slot empty'}), 409
    if not acquire():
        return jsonify({'error':'system busy'}), 423
    serial_ctrl.connect()
    serial_ctrl.send(f'OUT {s.slot} manual')
    logic.release_shelf(s)
    release()
    return jsonify({'ok':True})
