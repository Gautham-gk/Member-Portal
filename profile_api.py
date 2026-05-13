import json
#  this is for dealing with for example, convertin
import os
# os stands for operating system. this "module" is imported for checking if the database file exist
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()
# this is creating an "instance" of fastapi. In other words, we are telling the server that the api used here is FASTapi.


# --- DATABASE LOGIC (PERSISTENCE) ---
DB_FILE = "database.json"

# name of database file created.

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
             return json.load(f)
             # "with" is like a door which can "automatically close". so here, the with function opens the file for reading as variable "f" if it exists, and once it loads the data, file is "automatically closed".

    return [{"username": "admin", "bio": "Initial admin user"}]

# function laod_data will return the json file if it exists. Otherwise it will return username:admin and its bio.

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
        # save_data is the function for saving the file

# Initialize our data from the file
user_database = load_data()



# --- THE "FACE" (FRONTEND) ---
@app.get("/", response_class=HTMLResponse)
# app.get will tell the website that, if ppl go to homepage(/), they should be able to "read" the following. respnse_class=htmlresponse conveys website that the return value is html
def read_index():
    rows = ""
    for user in user_database:
        # okei this is niceeeeee! It adds the info of each user into the table 
        rows += f"""
        <tr>
            <td><b>{user['username']}</b></td>
            <td>{user['bio']}</td>
            <td>
                <a href="/edit/{user['username']}">Edit</a>
                |
                <!-- html forms do not support put or delete. the only available requests are GET and POST. -->
                <form action="/delete/{user['username']}" method="post" style="display:inline;">
                    <button type="submit" style="color: red;">Delete</button>
                </form>
            </td>
        </tr>
        """

    return f"""
    <html>
        <head><title>Member Portal</title></head>
        <body style="font-family: sans-serif; padding: 50px; text-align: center;">
            <h1>Member Portal</h1>
            
            <div style="max-width: 1200px; margin: auto; text-align: center;">
                <div style="text-align: left; background: #f9f9f9; padding: 20px; border-radius: 10px;">
                    <h3>Add New Member</h3>
                    <!-- post is gonna redirect the user to the /add page when the user clicks on the "Add to List" button. its not possible for user to access this page without clicking button. -->
                    <form action="/add" method="post">
                        Username: <input type="text" name="username" required>
                        Bio: <input type="text" name="bio" required>
                        <button type="submit">Add to List</button>
                    </form>
                </div>

                <hr style="margin: 30px 0;">
                
                <h3>All Members</h3>
                <table border="1" cellpadding="15" style="border-collapse: collapse; width: 100%; margin: auto; background: white;">
                <thead style="background: #eee;">
                    <tr>
                        <th>Username</th>
                        <th>Bio</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                    # rows variable informs python that this is where the username and bio are gonna be displayed.
                </tbody>
            </table>
            </div>
        </body>
    </html>
    """

# --- THE ACTIONS (BACKEND) ---


@app.post("/add")
def add_user(username: str = Form(...), bio: str = Form(...)):
    new_user = {"username": username, "bio": bio}
    user_database.append(new_user)
    save_data(user_database) # SAVE TO DISK!
    return HTMLResponse(content="User Added! <a href='/'>Go Back</a>", status_code=200)
    # appends user to user_database, and then saves the data to the database.json file. status_code=200 means that the request was PERFECT OK!.
    


@app.post("/delete/{username}")
def delete_user(username: str):
    for user in user_database:
        if user["username"] == username:
            user_database.remove(user)
            break
    save_data(user_database) # SAVE TO DISK!
    return HTMLResponse(content="User Deleted! <a href='/'>Go Back</a>", status_code=200)

    # delete_user is for deleting the entry 


@app.get("/edit/{username}", response_class=HTMLResponse)
def edit_page(username: str):
    #  this is for editing the bio of a user.
    target_user = next((u for u in user_database if u["username"] == username), None)
    # this is a for loop and if statement. The next here says "store the first user that satisfies the condition". If nothing satifies, it will return None. 
    if not target_user: return "User not found"

    return f"""
    <html>
        <body style="font-family: sans-serif; padding: 50px;">
            <h1>Edit Profile for {username}</h1>
            <!-- clicking save changes is basically a "post" request that will redirect user to /update/{{username}} page where the profile updated message would be shown, as in update_user function. -->
            <form action="/update/{username}" method="post">
                New Bio: <input type="text" name="new_bio" value="{target_user['bio']}" required>
                <button type="submit">Save Changes</button>
            </form>
            <p><a href="/">Cancel</a></p>
        </body>
    </html>
    """

@app.post("/update/{username}")
def update_user(username: str, new_bio: str = Form(...)):
    for user in user_database:
        if user["username"] == username:
            user["bio"] = new_bio
            break
    save_data(user_database) # SAVE TO DISK!
    return HTMLResponse(content="Profile Updated! <a href='/'>Go Back</a>", status_code=200)

@app.get("/json")
def get_json():
    return user_database
