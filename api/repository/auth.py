from fastapi import HTTPException,status
from models import models,schemas
from sqlalchemy.orm import Session
from sqlalchemy import and_,or_,not_
from utils import cryptoUtil
from datetime import datetime,timedelta

#auth crud operation
def create_reset_code(request:schemas.EmailRequest,reset_code:str,db:Session):
    query=f"""
    INSERT INTO codes(email,reset_code,status,expired_in)
    VALUES ('{request.email}','{reset_code}','1','{(datetime.now()+timedelta(hours=8))}');
"""
    db.execute(query)
    db.commit()

    return {"Message": f"Reset Code created successfully for User with email {request.email}."}

def reset_password(new_password:str,email:str,db:Session):
    query = f""""
        UPDATE user SET password ='{cryptoUtil.get_hash(new_password)}' WHERE email='{email}';
    """
    db.execute(query)
    db.commit()
    return {"Message": f"Password reset successful for User with email {email}."}

def disable_reset_code(reset_password_token:str,email:str,db:Session):
    query = f"""
    UPDATE codes
    SET status ='0'
    WHERE 
        status='1'
    AND
        reset_code='{reset_password_token}'
    OR
        email='{email}';
    """
    db.execute(query)
    db.commit()

    return {"Message": f"Reset code successfully disabled for User with email - {email}."}

def find_existed_user(email:str,db:Session):
    user = db.query(models.User).filter(and_(models.User.email==email,models.User.is_active ==True)).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Either user with email {email} not found OR currently in-active !")
    return user
def check_reset_