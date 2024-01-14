from fastapi import FastAPI
from routers.blog import blog as blog_router
from routers.user import user as user_router

app = FastAPI()

app.include_router(blog_router, prefix = "/blog", tags = ["Blogs"])
app.include_router(user_router, prefix = "/user", tags = ["Users"])


@app.get("/")
def home_page():
    return "Welcome to the No1 blog app in the world"

