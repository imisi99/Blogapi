import csv
from fastapi import APIRouter, Form, Depends, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field
from.blog import Authorize
from starlette import status
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


@user.post("/user-signup", status_code= status.HTTP_201_CREATED)
def user_signup(
    user : User):  
    user_create = False
    with open("u_data.csv", "a", newline='') as doc:
        writer = csv.writer(doc)
        writer.writerow([user.firstname, user.lastname, user.username, user.email, user.password])
        user_create = True
        if not user_create:
            raise HTTPException(status_code= 400, detail= "Bad Request")
        

        return f"{user.firstname} {user.lastname} Thank you for being a participant in this amazing blog"
    
        

@user.put("/forgot-password", status_code= status.HTTP_202_ACCEPTED)
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
            with open("u_data.csv", "w", newline= '')as doc:
                writer = csv.writer(doc)
                writer.writerow(header)
                for index, row in enumerate(rows):
                    if str(row[2]) == username:
                        writer.writerow([row[0], row[1], row[2], row[3], new_password])     
                    else:
                        writer.writerow(rows[index])

            return "Password changed successfully"
        
        else:
            raise HTTPException(status_code= 404, detail= "Username not found")
        
    else:
        raise HTTPException(status_code= 401, detail= "Unauthorized user")
    


@user.delete("/delete-user",status_code= status.HTTP_204_NO_CONTENT)
def delete_user(
    username : str,
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
                if str(row[2]) == username:
                    found = True

        if found:
            with open("u_data.csv", "w", newline= '') as docs:
                writer = csv.writer(docs)
                writer.writerow(header)
                for row in rows:
                    if str(row[2]) != username:
                        writer.writerow(row)
                
            return "User deleted successfully"
        else:
            raise HTTPException(status_code=404, detail="User not found")
    
    else:
        raise HTTPException(status_code= 401, detail= "Unauthorized user")

