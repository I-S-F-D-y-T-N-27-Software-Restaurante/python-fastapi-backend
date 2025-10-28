from pydantic import BaseModel


class UserLoginDTO(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {"email": "alice@example.com", "password": "pass123"}
        }


class TokenDTO(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    user_email: str
    roles: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "user_email": "alice@example.com",
                "roles": ["admin", "waiter"],
            }
        }


class UserTokenDataDTO(BaseModel):
    user_id: str
    user_email: str
    roles: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "user_email": "alice@example.com",
                "roles": ["admin", "waiter"],
            }
        }
