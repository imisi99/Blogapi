from fastapi import APIRouter, File, Form, UploadFile
from typing import Annotated

user = APIRouter()

@user.post("/")
async def user_singup(
    firstname :Annotated[str, Form()],
    lastname : Annotated[str, Form()],
    username : Annotated[str, Form()],
    email : Annotated[str, Form()],
    password : Annotated[str, Form()]

):

    return f"Dear {firstname} {lastname} , Thank you for being a participant in this amazing blog"