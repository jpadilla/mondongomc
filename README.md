mondongomc
==========

Simple dynamic REST API. This might be useful when developing client-side apps and really don't need a backend to start

![You can't touch this](http://24.media.tumblr.com/tumblr_m1jr11yhr11qi0cuno1_500.gif)

## Getting Started
```
pip install -r requirements.txt
mongod run
python mondongomc.py
```

### Creating a document
```
curl --dump-header - -X POST --data '{"name": "Ferrari", "year": 2013}' http://localhost:5000/car/
```
This will take care of creating the collection "car" and a document with that data.
