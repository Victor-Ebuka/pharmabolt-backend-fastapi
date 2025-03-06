from auth import get_current_user
from crud.cart import get_cart_by_user_id
from database.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud.users import add_user, delete_user, get_user_by_email, get_user_by_id, get_user_by_phone_no, get_user_by_phone_no_and_email, get_user_profile, get_users, update_user
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Add a new user
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = add_user(user, db)
    return new_user

# Get all users
@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(skip, limit, db)
    return users

# Get a specific user by ID
@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(user_id, db)
    return user

# Search for a specific user by email or phone number
@router.post("/search", response_model=UserResponse)
def search_user(email: str = None, phone_no: str = None, db: Session = Depends(get_db)):
    if email and phone_no:
        user = get_user_by_phone_no_and_email(phone_no, email, db)
    elif email:
        user = get_user_by_email(email, db)
        return user
    elif phone_no:
        user = get_user_by_phone_no(phone_no, db)
    elif not email and not phone_no:
        raise HTTPException(status_code=400, detail="Please provide an email or phone number")
    return user
    
# Get user profile
@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    return get_user_profile(current_user, db)

# Update user profile
@router.put("/profile")
def update_profile(user: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = update_user(user, current_user, db)
    return user

# Delete user profile
@router.delete("/profile")
def delete_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if delete_user(current_user.id, db):
        return {"message": "User deleted successfully"}