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
    

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(...)
    confirm_password: str = Field(...)

    @field_validator("old_password")
    @classmethod
    def validate_old_password(cls, v: str):
        if not v or not v.strip():
            raise ValueError("Old password is required")
        return v

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str):
        if not v or not v.strip():
            raise ValueError("New password is required")
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, v: str):
        if not v or not v.strip():
            raise ValueError("Confirm password is required")
        return v

    @model_validator(mode="after")
    def check_passwords(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")

        if self.old_password == self.new_password:
            raise ValueError("New password must be different from old password")

        return self