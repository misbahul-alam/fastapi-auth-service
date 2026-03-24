from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field


class RegisterRequest(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr
    password: str = Field(...)
    confirm_password: str = Field(...)

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v: str):
        if not v or not v.strip():
            raise ValueError("This field is required")
        if len(v.strip()) < 2:
            raise ValueError("Must be at least 2 characters")
        return v.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if not v:
            raise ValueError("Password is required")
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(...)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if not v or not v.strip():
            raise ValueError("Password is required")
        return v