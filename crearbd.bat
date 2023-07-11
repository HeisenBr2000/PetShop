call C:\ProyectosDjango\TiendaPetShopFinal_venv\Scripts\activate.bat
call rmdir /s /q C:\ProyectosDjango\TiendaPetShopFinal\core\migrations
call python manage.py makemigrations
call python manage.py makemigrations core
call python manage.py migrate
call python manage.py migrate core
