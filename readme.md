# Django Start Project By Murodalidev

## Odatiy usulda kodni yuritish:
#### 1. Linux OS
```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements/local.txt
python manage.py runserver
```

#### 2. Windows OS
```shell
py -m venv venv
venv\Scripts\activate
pip install -r requirements/local.txt
py manage.py runserver
```

### Doker bilan o'ralgan kodni Local rejimda yuritish
```shell
sudo docker compose -f local.yml up --build
```

### Doker bilan o'ralgan kodni Production rejimda yuritish
```shell
sudo docker compose -f production.yml up --build 
```

### Doker bilan o'ralgan kodni Production rejimda Detached yuritish
```shell
sudo docker compose -f production.yml up --build -d
```