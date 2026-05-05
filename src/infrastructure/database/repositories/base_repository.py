from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, model):
        self.db.add(model)
        return model

    def remove(self, model):
        self.db.delete(model)

    def commit(self):
        self.db.commit()

    def flush(self):
        self.db.flush()

    def refresh(self, model):
        self.db.refresh(model)
        return model