from flask import Blueprint, request, jsonify
from services.queue_manager import QueueManager

bp = Blueprint('queue_controller', __name__)
qm = QueueManager()

@bp.route('/', methods=['GET'])
def list_queue():
    q = qm.list()
    return jsonify([{'id':j.id, 'type':j.job_type, 'sku':j.sku, 'created_at':str(j.created_at)} for j in q])

@bp.route('/enqueue', methods=['POST'])
def enqueue():
    data = request.json
    job_type = data.get('type')
    sku = data.get('sku')
    requested_by = data.get('requested_by')
    if job_type not in ('IN','OUT'):
        return jsonify({'error':'invalid type'}), 400
    job = qm.enqueue(job_type, sku, requested_by)
    return jsonify({'ok':True, 'id':job.id})

@bp.route('/<int:job_id>', methods=['DELETE'])
def remove(job_id):
    ok = qm.remove(job_id)
    return jsonify({'ok':ok})
