from fastapi import APIRouter

blog = APIRouter()

@blog.get("/")
def blog_home():
    return "Welcome to Imisioluwa blog channel"



@blog.get("/about")
def about():
    return "Banky"