from pydantic_settings import BaseSettings

class Settings(BaseSettings):
   
    DATABASE_URL: str = "postgresql://audit_admin:secure_dev_password@postgres:5432/compliance_vault"
    PROJECT_NAME: str = "Compliance Audit Engine"
    
    class Config:
        case_sensitive = True

settings = Settings()