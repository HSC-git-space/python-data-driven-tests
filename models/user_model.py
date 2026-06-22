from pydantic import BaseModel, EmailStr
from typing import Optional


class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None


class Company(BaseModel):
    name: Optional[str] = None


class UserModel(BaseModel):
    id: Optional[int] = None
    name: str
    username: Optional[str] = None
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[Address] = None
    company: Optional[Company] = None


class CreateUserModel(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None