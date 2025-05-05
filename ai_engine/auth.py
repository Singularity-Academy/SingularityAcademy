import os
import time
import jwt

# Same default secret key as Go backend
DEFAULT_SECRET_KEY = "AISAISAAA"
SECRET_KEY_FILE = "backend/auth_secret.key"

class AuthManager():
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    @classmethod
    def from_env(cls):
        # Try to read the secret key from file first
        secret_key = None
        try:
            if os.path.exists(SECRET_KEY_FILE):
                with open(SECRET_KEY_FILE, 'rb') as f:
                    secret_key = f.read()
                print(f"Secret key loaded from {SECRET_KEY_FILE}")
        except Exception as e:
            print(f"Error reading secret key file: {e}")
        
        # If file reading failed, try environment variable
        if not secret_key:
            secret_key = os.getenv("AUTH_SECRET_KEY")
            
        # If neither worked, use default
        if not secret_key:
            print("Could not load secret key from file or environment, using default key")
            secret_key = DEFAULT_SECRET_KEY
            
        return cls(secret_key)

    def verify_token(self, token: str) -> bool:
        try:
            # Decode the JWT token directly without additional JSON parsing
            # The Go backend uses HS256 algorithm with Claims structure
            claims = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Check the issuer matches what the Go backend sets
            if claims.get("iss") != "aiLearn":
                return False
                
            # Check if token is expired based on the exp claim
            if "exp" in claims and claims["exp"] < int(time.time()):
                return False
                
            # Ensure the user ID exists in the token
            if "ID" not in claims:
                return False
                
            return True
        except jwt.InvalidTokenError:
            return False
