from models import get_db, QueueJob
from sqlalchemy import asc

class QueueManager:
    def __init__(self):
        self.db = get_db()

    def enqueue(self, job_type, sku, requested_by=None, priority=100):
        job = QueueJob(job_type=job_type, sku=sku, requested_by=requested_by, priority=priority)
        self.db.add(job)
        self.db.commit()
        return job

    def dequeue(self):
        return self.db.query(QueueJob).order_by(asc(QueueJob.priority), asc(QueueJob.created_at)).first()

    def list(self, limit=50):
        return self.db.query(QueueJob).order_by(asc(QueueJob.priority), asc(QueueJob.created_at)).limit(limit).all()

    def remove(self, job_id):
        job = self.db.query(QueueJob).get(job_id)
        if job:
            self.db.delete(job)
            self.db.commit()
            return True
        return False
