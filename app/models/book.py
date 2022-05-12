from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id')) #singular author
    author = db.relationship("Author", back_populates="books")
    

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }