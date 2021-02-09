# Netguru Transfer System
This is a system that allows secure transfer of pictures and urls.

## Installation

Step by step.

1. Clone repository
```
git clone git@github.com:Brzydal/netguru.git
```
or
```
git clone https://github.com/Brzydal/netguru.git
```

2. Install required dependencies
```
cd netguru
pip install -r requirements.txt
```

3. Apply migrations
```python
python manage.py migrate
```

4. Start local server
```python
python manage.py runserver
```

5. Go to http://localhost:8000 and enjoy...

## Users

### Create first user by command
```python
python manage.py createsuperuser
```

#### Other users You can create in the same way or use Django Admin

 - Login URL: http://localhost:8000/accounts/login/
 - Logout URL: http://localhost:8000/accounts/logout/
 - Home URL:http://localhost:8000/
 
## Tests

### You can run test with command
```python
python manage.py test
```

## Admin

### Transfers can be managed from Django admin

 - Transfers URL: http://localhost:8000/admin/transfer/transfer/
 - User Agent URL : http://localhost:8000/admin/transfer/useragent/


## API

### You can also use system via API provided

 - Transfer CreateURL: http://localhost:8000/api/create/
 - Statistics URL : http://localhost:8000/api/statistics/