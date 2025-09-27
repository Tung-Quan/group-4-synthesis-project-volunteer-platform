import fastapi 


app = fastapi.FastAPI()

class DataBase:
    def __init__(self):
        self.users = []
        self.events = []
        if not hasattr(self.__class__, "__instance__"):
            self.__class__.__instance__ = self

    def get_instance(self):
        return self.__class__.__instance__
    
    def modify_data(self, data_type, data, METHOD="POST"):
        if data_type == "user" and METHOD == "POST":
            self.users.append(data)
        elif data_type == "event" and METHOD == "POST":
            self.events.append(data)
        else:
            raise ValueError("Invalid data type")
    
    def retrieve_data(self, data_type):
        if data_type == "user":
            return self.users
        elif data_type == "event":
            return self.events
        else:
            raise ValueError("Invalid data type")

db = DataBase()


# Define API endpoints
# LOGIN, REGISTER, PROFILE APIs

#
@app.get("/login")
def login():
    return {"message": "Login successful"}
  
@app.get("/register")
def register():
    return {"message": "Registration successful"}
  
@app.get("/profile")
def profile():
    return {"message": "User profile data"} 


# EVENT APIs
@app.get("/events")
def events():
    return {"message": "List of events"}