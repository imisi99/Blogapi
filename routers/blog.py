import csv
from typing import Optional 
from fastapi import APIRouter, Form, Depends, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from starlette import status

blog = APIRouter()



class Create(BaseModel):
    title : str
    body : str
    author : str
    created_at : datetime 

    # class Config():
    #     json_schema_extra = {
    #         'example' : {
    #             "title" : "title",
    #             "body" : "body",
    #             "author" : "author"
    #         }
    #     }


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
@blog.get("/", status_code= status.HTTP_200_OK)
def blog_home():
    rows = []
    with open("data.csv", "r") as docs:
        reader = csv.reader(docs)

        next(reader)

        for row in reader:
            rows.append(row)
    return rows
            




#About Page
@blog.get("/about", status_code=status.HTTP_200_OK)
def about_page():
    return {
        "About us":"We are a global community spreading true real-life information about the current global situation, for as the say information is power. This website was founded on the 25th of October 2023 in the aim to maximize the full potentials of youth.",
        "Our Mission" : "To ensure that there is no one out there lacking information.",
        "Our Vision" : "A world of peace and harmony."
    }



#Contact Page
@blog.get("/contact", status_code=status.HTTP_200_OK)
async def contact_page():
    return {
    "message":"You can reach us across the following social media platform",
    "instagram" : "BLOG_API",
    "Facebook" : "BLOG_API",
    "whatsapp no" : +2348012345678
}


#get blogs by the title
@blog.get("/{title}",status_code=status.HTTP_200_OK)
async def get_blog_by_title(
    title:str, 

):
   with open("data.csv","r") as docs:
        reader = csv.reader(docs)
        next(reader)
        for row in reader:
            if (row[0]) == title:
                return Create (title=(row[0]), body=row[1], author = (row[2]), created_at = (row[3]))
        
        raise HTTPException(status_code=404, detail="Blog not found")



#Create a Blog
@blog.post("/create",status_code= status.HTTP_201_CREATED)
async def create_blog(
    blog : Create,
    authorized : bool = Depends(Authorize)
):  
    blog_create = False
    if authorized:
        timestamp = datetime.now()
        with open("data.csv", "a", newline='') as docs:
            writer = csv.writer(docs)
            writer.writerow([blog.title, blog.body, blog.author, timestamp])
            blog_create = True

        if not blog_create:
            raise HTTPException(status_code=400, detail="Bad Request")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized user")

 

#Edit Blog
@blog.put("/edit",status_code= status.HTTP_202_ACCEPTED)
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
            with open("data.csv", "w",newline= '') as docs:
                writer = csv.writer(docs)
                writer.writerow(header)
                for index, row in enumerate(rows):
                    if str(row[0]) == title :
                        writer.writerow([blog.title, blog.body, blog.author, blog.created_at])
                    else:
                        writer.writerow(rows[index])

            return"Blog Edited Successfully"
        else:
            raise HTTPException(status_code=404, detail="Blog not found")
        
    else:    
       raise HTTPException(status_code=401, detail="Unauthorized user")



#To delete blog
@blog.delete("/delete",status_code= status.HTTP_204_NO_CONTENT)
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
            with open ("data.csv", "w",newline= '') as docs:
                writer = csv.writer(docs)
                writer.writerow(header)
                for index, row in enumerate(rows):
                    if str(row[0]) == title:
                        continue
                    else:
                        writer.writerow(rows[index])
                           
            return "Blog deleted successfully."
        else:
            raise HTTPException(status_code=404, detail="Blog not found")
    
    else:
        raise HTTPException(status_code=401, detail="Unauthorized user")