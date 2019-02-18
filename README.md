# school-admin
Administration system for student registration and notification

```
mysql -u root -p schooladmin < sql/build_db.sql
python src/controller.py

mysql -u root -p < sql/build_test_db.sql
python -m unittest discover
```