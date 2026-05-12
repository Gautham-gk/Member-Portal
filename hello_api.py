from fastapi import FastAPI

# 1. Create the "App" (This is your web server)
app = FastAPI()

# start a new web application, calling it app.

# 2. Create a "Route" (A path on the website)
# This is the "Home" page (/)

@app.get("/")
def read_root():
    return {"message": "Welcome to your first API!", "status": "Learning Mode Active"}

# 3. Create a dynamic "Route"
# This takes a name from the URL and says hello
@app.get("/greet/{name}")
def greet_user(name: str):
    return {
        "greeting": f"Hello, {name}!",
        "note": "You just successfully sent data to a server and got a response back!"
    }
