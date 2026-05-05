 TESS BOSKU


 oke baik
NOTE:
AKUN INI ADA 3 WEB
1. PETANI MITRA
2. DONATUR
3. ADMIN login lewan url /admin-login/
   untuk akun admin di buat di terminal ketik
   python manage.py createsuperuser
   lalu masukan sesuai intruksinya

untuk menjalankan web jangan login 3 akun sekaligus dalam 1 device karena projek web ini belum dideploy

CAEA MENJALANKAN PROJEK INI:
1. clone projek ini

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

Penjelasan tiap bagian:
isi env
DB_USER=postgres.ubuopbjsyasayshgttbp
DB_PASSWORD=JejakaDaya&12
DB_HOST=aws-1-ap-southeast-1.pooler.supabase.com
DB_PORT=6543
SECRET_KEY → kunci rahasia Django (harus diisi sendiri)
DEBUG → gunakan True untuk development


Cara membuat SECRET_KEY:

Jalankan perintah berikut di terminal:

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Lalu copy hasilnya ke bagian SECRET_KEY di file .env.


DAN INSTAL DOTENV
pip install python-dotenv


6. pip install psycopg2-binary
7. Jalanin server
python manage.py runserver

8. SET UP TAILDWIN
   a. npm install
   b. npm run dev