# SQLaboratory

## What is it?

**SQLaboratory is a simple way to work with SQLAlchemy library**

The idea behind is to write code like you would write SQL

## How to use it
### Select example in SQLab:
**main.py**
```python
from sqlaboratory import SQLab
from users import Users

SQLab.connect("sqlite:///test.db")

res = SQLab.select_from(Users, 
	_select = Users.name, 
	_where = Users.id < 3, 
	_orderby = Users.id, 
	_limit = 1)

print(res)
# [('John',)]
```

**users.py**
```python
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

from sqlaboratory import SQLab, Base

class Users(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String, unique=True)

	def __repr__(self) -> str:
			return f"Users(id={self.id} name={self.name})\n\n"
```

### Create, Update, Delete:
**main.py**
```python
from sqlab import SQLab
from users import Users

SQLab.connect("sqlite:///test.db")

SQLab.create(Users(name = "Simon"))
SQLab.update(Users, {"name" : "BetterSimon"}, _where = Users.name == "Simon")
res = SQLab.select_from(Users)
print(res)
# [Users(id=1 name=John), Users(id=2 name=BetterSimon)]

SQLab.delete(Users, _where = Users.name == "BetterSimon")
res = SQLab.select_from(Users)
print(res)
# [Users(id=1 name=John)]
```

### Complex queries:
**main.py**
```python
from sqlab import SQLab
from users import Users

SQLab.connect("sqlite:///test.db")

SQLab.create(Users(name = "Simon")) # 2
SQLab.create(Users(name = "Anne"))  # 3
SQLab.create(Users(name = "Peter")) # 4
SQLab.create(Users(name = "Kate"))  # 5
SQLab.create(Users(name = "Alice")) # 6
SQLab.create(Users(name = "Alex"))  # 7
SQLab.create(Users(name = "Ben"))   # 8

res = SQLab.select_from(
	_from = Users,
	_select = [Users.name, Users.id],
	_where = (Users.id > 3) & ((Users.id.in_([4, 5]) | (Users.id == 7))),
	_orderby = [Users.name, Users.id.desc()],
	_limit = 3)
print(res)
# [('Alex', 7), ('Kate', 5), ('Peter', 4)]
```

### Get select query (use -limit):
**main.py**
```python
from sqlab import SQLab
from users import Users

SQLab.connect("sqlite:///test.db")

res = SQLab.select_from(
	_from = Users,
	is_query=True)
# SELECT users.id AS users_id, users.name AS users_name 
# FROM users
```

## What is missing

- **JOINs**
- **SQL functions**
- **Table operations**