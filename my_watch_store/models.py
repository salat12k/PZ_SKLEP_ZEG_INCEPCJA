from . import db

class Watch(db.Model):
    __tablename__ = 'watches'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=True)
    # Nazwa pliku (np. "photo.jpg") przechowywana w bazie
    image_filename = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Watch brand={self.brand}, model={self.model}, price={self.price}, image={self.image_filename}>"
