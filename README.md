ИНСТРУКЦИЯ ПО ЗАПУСКУ:

1. Находим каталог с базами данных:
sudo -u postgres psql -c "SHOW data_directory;"

2. Создаем файл audit_db.py и копируем в него код скрипта:
nano audit_db.py

2.1. Создаем файл requirements.txt и копируем в него информацию о зависимостях
nano requirements.txt

3. Редактируем конфигурацию в файле audit_db.py под свою ситуацию:
DATA_DIR = "/var/lib/postgresql/16/main"
BASE_DIR = os.path.join(DATA_DIR, "base")
DB_USER = "postgres"
DB_PASSWORD = "YOUPASSWORD"
DB_HOST = "localhost"

POSTGRES_CONF = "/etc/postgresql/16/main/postgresql.conf"
HBA_CONF = "/etc/postgresql/16/main/pg_hba.conf"
SSL_CERT = "/etc/ssl/certs/ssl-cert-snakeoil.pem"
SSL_KEY = "/etc/ssl/private/ssl-cert-snakeoil.key"

4. Создаем и активируем виртуальное окружение, устанавливаем библиотеки:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
опционально (если пакеты не скачиваются):
pip install -r requirements.txt -i https://mirror.yandex.ru/mirrors/pypi/simple/

6. Предоставляем пользователю Postgres (если требуется) права доступа к папке и файлам скриптов (изменяем путь, если необходимо):
chmod o+x ~ && chmod o+rx ~/CheckDB && chmod o+r ~/CheckDB/*.py

7. Запускаем:
sudo -u postgres ./venv/bin/python audit_db.py

8. Деактивируем виртуальное окружение и удаляем созданные файлы (если требуется):
deactivate
rm -rf audit_db.py requirements.txt venv __pycache__ .env pg_audit_flowchart.*

ОПИСАНИЕ РАБОТЫ:

1. Первая таблица Databases (OID vs Name vs Size)
Отображает список баз данных PjstgreSQL, их наименование OID и размер.

2. PostgreSQL Security Check
Эта функция выполняет базовый аудит конфигурации PostgreSQL на уровне файловой системы, соответствие требованиям безопасности (CIS PostgreSQL Benchmark).
Права доступа к критически важным файлам:
postgresql.conf — основной конфигурационный файл;
pg_hba.conf — файл управления доступом;
data_directory — директория с данными БД;
SSL-сертификаты (.pem, .key).
Наличие и корректность прав:
Только владелец должен иметь права на чтение/запись (600, 640, 700);
Файлы SSL должны существовать;
Проверка защиты приватного ключа;
Проверка срока действия сертификата.
Выводит таблицу с результатами:
✔️ — всё в порядке;
❌ — найдены нарушения (например, слишком широкие права доступа или отсутствующий файл).

3. Security audit 
Функция выполняет безопасностный аудит конкретной базы данных PostgreSQL, используя системные представления (pg_roles, pg_extension, pg_namespace).
Подключается к указанной базе данных с помощью psycopg2.
Проверяет ключевые параметры безопасности:
Проверка	Описание
SUPERUSER roles	Перечисляет всех пользователей с флагом SUPERUSER (полные права)
REPLICATION roles	Роли с флагом REPLICATION (могут копировать данные)
Extensions	Список установленных расширений PostgreSQL
Schemas with CREATE for PUBLIC	Список схем, где PUBLIC (все пользователи) имеют право CREATE
Использует has_schema_privilege() для точной проверки прав CREATE в схемах от имени public.
Выводит таблицу отчета, где:
Check – название проверки;
Result – результат (список ролей, расширений или None, если не обнаружено).
