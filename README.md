# User-search-history

#### Download the code to your PC, unpack the zip and move inside the folder.

#### 1. Create a new Python Virtual Environment:
```
python3 -m venv venv
```

#### 2. Activate the environment and install all the Python/Django dependencies:

```
source ./venv/bin/activate
pip install -m ./requirements.txt
```

### 3. Create a Mongodb database named "search_history"


### 4. Apply the migrations as usual (At first, go inside the project directory.  ```cd User-seach-history```).
```
python manage.py makemigations
python manage.py migrate
```
#### 5. To run application server 
```
python manage.py runserver
```
#### 6. To populate database, run
```
python populate.py
```

#### 7. Find live version [here](https://search-history.herokuapp.com/)

