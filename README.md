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
```bash
uvicorn warehouse/main:app --reload
```

```bash
python shop/manage.py createsuperuser
```

```bash
python shop/manage.py generate_books 10
```


