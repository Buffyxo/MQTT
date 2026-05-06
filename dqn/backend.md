# Backend helper

## venv

This project uses a virtual environment. To create Virtual environment run this command:

> python -m venv .venv

To activate the venv run this command:

> .venv\scripts\activate

Your console now look similar to this:

> (.venv) C:\Users\user\COS40006\backend>

Virtual environment is now ready to allow installation of packages

## Routes

To allow the frontend to interact with the backend, fastAPI is used.

### Running

To run the fastAPI first connect to the venv. Once your in the virtual environment, use this command to run the server:

> fastapi dev app/routes/routes.py

### Usage

All responses must be wrapped in a JSONResponse with appropriate status code, message (Short summary), body (Returning any data must under the body) 

#### Examples

```
@app.get("/endpoint")
def read_data():
    ...
    return JSONResponse(status_code=status_code, content={"message": "message", "body":{data}})
```

```
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

```

## requirements.txt

To ensure all users know which packages need to be installed please update the requirements.txt. To update it enter the virtual environment then run this:

> pip freeze > requirements.txt

Now any user missing all the packages can run this command to install all missing packages:

> pip install -r requirements.txt