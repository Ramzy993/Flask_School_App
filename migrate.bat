rmdir /S /Q migrations
python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrate
