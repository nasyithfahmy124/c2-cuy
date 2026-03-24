cara menjalankan projek
1. clone
2 aktifkan env
python -m venv env
3.install dependency
pip install -r requirements.txt
4. Copy file environment

Project ini menggunakan file .env untuk menyimpan konfigurasi seperti database dan secret key.

Karena file .env bersifat rahasia, file tersebut tidak disertakan di repository.
Sebagai gantinya, disediakan file .env.example sebagai template.

Cara membuat file .env:
Untuk Windows (CMD / PowerShell):

copy .env.example .env

Untuk Linux / Mac:

cp .env.example .env

5. Isi file .env

Setelah file .env dibuat, buka file tersebut lalu isi sesuai konfigurasi di komputer masing-masing.

Contoh:

DB_NAME=db_green
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

SECRET_KEY=isi_dengan_secret_key_kamu
DEBUG=True

Penjelasan tiap bagian:
DB_NAME → nama database yang kamu buat di MySQL
DB_USER → username database (biasanya root)
DB_PASSWORD → password database (kosong jika tidak pakai password)
DB_HOST → biasanya localhost
DB_PORT → default MySQL 3306
SECRET_KEY → kunci rahasia Django (harus diisi sendiri)
DEBUG → gunakan True untuk development
Cara membuat SECRET_KEY:

Jalankan perintah berikut di terminal:

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Lalu copy hasilnya ke bagian SECRET_KEY di file .env.

6. migrasi Migrasi database
python manage.py migrate
7. Jalanin server
python manage.py runserver