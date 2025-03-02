from crud.cart import get_cart_by_user_id
from database.session import get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from crud.users import add_user, get_user_by_id, get_users
from models.user import User
from schemas.user import UserCreate, UserResponse

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
    cart = get_cart_by_user_id(user_id, db)
    user.cart = cart
    return user