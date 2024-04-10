from fastapi import FastAPI
from fastapi.middlewares.cors import CORSMiddleware
from . import models
from utils.dbUtil import engine
from routes import auth,user,admin 

#database connection initialization
models.Base.metadata.create_all(bind=engine)

#app initialization
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#register route for authentication
app.include_router(auth.router)
#register route for admin
app.include_router(admin.router)
#register route for user
app.include_router(user.router)

