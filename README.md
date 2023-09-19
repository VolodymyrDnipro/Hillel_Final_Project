## Django Shop Setup Guide
### This guide will help you set up the Django Shop project on your local machine.

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Run the Development Server
```bash
python shop/manage.py runserver
```
#### Step 3: Apply Migrations
```bash
python shop/manage.py makemigrations
```
```bash
python shop/manage.py migrate
```
```bash
python shop/manage.py createsuperuser
```

```bash
python shop/manage.py generate_books 10
```
#
#### Step 2: Run the Development Server
```bash
python warehouse/manage.py runserver 8080
```
#### Step 3: Apply Migrations
```bash
python warehouse/manage.py makemigrations
```
```bash
python warehouse/manage.py migrate
```
```bash
python warehouse/manage.py createsuperuser
```
```bash
python warehouse/manage.py generate_books 10
```


