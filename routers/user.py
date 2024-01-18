import csv
from fastapi import APIRouter, Form, Depends
from typing import Annotated
from pydantic import BaseModel, Field
from.blog import Authorize
user = APIRouter()


class User(BaseModel):
    firstname : Annotated[str, Field(min_length= 3)]
    lastname : Annotated[str, Field(min_length= 3)]
    username : Annotated[str, Field(min_length=3, max_length=15)]
    email : Annotated[str, Field()]
    password : Annotated[str, Field(min_length=8)]


def User_Authorize(
    username : str
):
    with open("u_data.csv", "r")as docs:
        reader = csv.DictReader(docs)
        for row in reader:
            if row["username"] == username:
                return True

    return False


@user.post("/")
def user_signup(
    user : User

):
    with open("u_data.csv", "a", newline='') as doc:
        writer = csv.writer(doc)
        writer.writerow([user.firstname, user.lastname, user.username, user.email, user.password])
        
    return f"{user.firstname} {user.lastname} Thank you for being a participant in this amazing blog"
    
@user.put("/forgot-password")
def change_password(
    username : str,
    new_password : str = Form(...),
    authorized : bool = Depends(User_Authorize)
):
    if authorized:
        rows = []
        found = False
        with open("u_data.csv", "r") as doc:
            reader = csv.reader(doc)
            header = next(reader)
            for row in reader:
                rows.append(row)
                if str(row[2]) == username:
                    found = True
            
        if found:
            with open("u_data.csv", "w")as doc:
                writer = csv.writer(doc)
                writer.writerow(header)
                for index, row in enumerate(rows):
                    if str(row[2]) == username:
                        writer.writerow([row[0], row[1], row[2], row[3], new_password])     
                    else:
                        writer.writerow(rows[index])

            return "Password changed successfully"
    else:
        return "Username Incorrect, Try again."

@user.delete("/delete-user")
def delete_user(
    authorized : bool = Depends(Authorize)
):
    if authorized:
        rows = []
        found = False
        with open("u_data.csv", "r") as docs:
            reader = csv.reader(docs)
            header = next(reader)
            for row in reader:
                rows.append(row)
                if str(row[2]) == Authorize.get("username") and str(row[4]) == Authorize.get("password"):
                    found = True

        if found:
            with open("u_data.csv", "w") as docs:
                writer = csv.writer
                writer.writerow(header)
