from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Konfiguracja bazy danych – w tym przypadku SQLite (plik watch_store.db)
# Można też użyć innego silnika bazodanowego, np. PostgreSQL czy MySQL.
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'watch_store.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Model (tabela) w bazie danych
class Watch(db.Model):
    __tablename__ = 'watches'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Watch brand={self.brand}, model={self.model}>"

# Tworzymy wszystkie tabele (jeśli nie istnieją)
with app.app_context():
    db.create_all()

# Strona główna – wyświetla listę zegarków
@app.route('/')
def home():
    watches = Watch.query.all()
    return render_template('home.html', watches=watches)

# Formularz dodawania nowego zegarka
@app.route('/add', methods=['GET', 'POST'])
def add_watch():
    if request.method == 'POST':
        brand = request.form.get('brand')
        model = request.form.get('model')

        # Tworzymy obiekt zegarka i zapisujemy do bazy
        new_watch = Watch(brand=brand, model=model)
        db.session.add(new_watch)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html')

# Usuwanie zegarka o podanym id
@app.route('/delete/<int:watch_id>', methods=['POST'])
def delete_watch(watch_id):
    watch_to_delete = Watch.query.get_or_404(watch_id)
    db.session.delete(watch_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
