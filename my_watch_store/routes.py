import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

from . import db
from .models import Watch

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Strona główna - wyświetla listę zegarków."""
    watches = Watch.query.all()
    return render_template('home.html', watches=watches)


@main_bp.route('/add', methods=['GET', 'POST'])
def add_watch():
    """Dodawanie nowego zegarka."""
    if request.method == 'POST':
        # Pobieramy dane z formularza
        brand = request.form.get('brand')
        model = request.form.get('model')
        price_str = request.form.get('price')

        # Konwersja ceny
        try:
            price = float(price_str)
        except (ValueError, TypeError):
            price = 0.0

        # Pobieramy przesłany plik
        file = request.files.get('image')
        image_filename = None

        if file and file.filename:
            # Zabezpieczamy nazwę pliku
            filename = secure_filename(file.filename)
            # Budujemy pełną ścieżkę do zapisu
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            # Zapis pliku na dysk
            file.save(upload_path)
            # W bazie będziemy przechowywać tylko nazwę pliku
            image_filename = filename

        # Tworzymy nowy obiekt Watch
        new_watch = Watch(
            brand=brand,
            model=model,
            price=price,
            image_filename=image_filename
        )
        db.session.add(new_watch)
        db.session.commit()

        return redirect(url_for('main.home'))

    return render_template('add.html')


@main_bp.route('/delete/<int:watch_id>', methods=['POST'])
def delete_watch(watch_id):
    """Usuwanie zegarka z bazy i kasowanie pliku z dysku."""
    watch_to_delete = Watch.query.get_or_404(watch_id)

    # Jeśli zegarek ma plik, usuwamy go z dysku
    if watch_to_delete.image_filename:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], watch_to_delete.image_filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.session.delete(watch_to_delete)
    db.session.commit()
    return redirect(url_for('main.home'))
