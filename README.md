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
