import csv 
from fastapi import APIRouter, Form, Depends
from pydantic import BaseModel
from datetime import datetime


blog = APIRouter()



class Create(BaseModel):
    title : str
    body : str
    author : str
    created_at : datetime


def Authorize(
    username: str, 
    password: str
):
    with open("u_data.csv", "r") as docs:
        reader = csv.DictReader(docs)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                return True
    return False

#Get all blogs
@blog.get("/")
def blog_home():
    rows = []
    with open("data.csv", "r") as docs:
        reader = csv.reader(docs)

        next(reader)

        for row in reader:
            rows.append(row)
    return rows
            




#About Page
@blog.get("/about")
def about_page():
    return {
        "About us":"We are a global community spreading true real-life information about the current global situation, for as the say information is power. This website was founded on the 25th of October 2023 in the aim to maximize the full potentials of youth.",
        "Our Mission" : "To ensure that there is no one out there lacking information.",
        "Our Vision" : "A world of peace and harmony."
    }



#Contact Page
@blog.get("/contact")
async def contact_page():
    return {
    "message":"You can reach us across the following social media platform",
    "instagram" : "BLOG_API",
    "Facebook" : "BLOG_API",
    "whatsapp no" : +2348012345678
}


#get blogs by the title
@blog.get("/{title}")
async def get_blog_by_title(
    title:str, 

):
   with open("data.csv","r") as docs:
        reader = csv.reader(docs)
        next(reader)
        for row in reader:
            if (row[0]) == title:
                return Create (title=(row[0]), body=row[1], author = (row[2]), created_at = (row[3]))
        return "Blog not found"



#Create a Blog
@blog.post("/create")
async def create_blog(
    blog : Create,
    authorized : bool = Depends(Authorize)
):
    if authorized:
        timestamp = datetime.now()
        with open("data.csv", "a", newline='') as docs:
            writer = csv.writer(docs)
            writer.writerow([blog.title, blog.body, blog.author, timestamp])
        return "Blog Published Successfully"
    else:
        return "Username or Password wrong, Click the change password route to change password if forgotten or click the signup route to signup if not a user  . "



#Edit Blog
@blog.put("/edit")
async def edit_blog(
    blog : Create,
    title : str,
    authorized : bool = Depends(Authorize)

):  
    if authorized:
        rows = []
        found = False
        with open("data.csv", "r") as docs:
            reader = csv.reader(docs)
            header = next(reader)
            for row in reader:
                rows.append(row)
                if str(row[0]) == title:
                    found = True
        if found:       
            with open("data.csv", "w") as docs:
                writer = csv.writer(docs)
                writer.writerow(header)
                for index, row in enumerate(rows):
                    if str(row[0]) == title :
                        writer.writerow([blog.title, blog.body, blog.author, blog.created_at])
                    else:
                        writer.writerow(rows[index])

            return"Blog Edited Successfully"
    else:
        return "Username or Password wrong, Click the change password route to change password if forgotten or click the signup route to signup if not a user  . "



#To delete blog
@blog.delete("/delete")
async def delete_blog(
    title : str = Form(...),
    authorized : bool = Depends(Authorize)
):
    if authorized:
        rows = []
        found = False
        with open("data.csv", "r") as docs:
            reader = csv.reader(docs)
            header = next(reader)
            for row in reader:
                rows.append(row)
                if str(row[0]) == title:
                    found = True

        if found:
            with open ("data.csv", "w") as docs:
                writer = csv.writer(docs)
                writer.writerow(header)
                for index, row in enumerate(rows):
                    if str(row[0]) == title:
                        continue
                    else:
                        writer.writerow(rows[index])
                           
            return "Blog deleted successfully."
        else:
            return "Blog not found"
    
    else:
        return "Username or Password wrong, Click the change password route to change password if forgotten or click the signup route to signup if not a user  . "