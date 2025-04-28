import os
from time import time
import jwt

class AuthManager:
    def __init__(self, secret: str):
        self.secret = secret

    @classmethod
    def from_env(cls):
        secret = os.getenv("JWT_SECRET_KEY")
        if not secret:
            raise ValueError("JWT_SECRET_KEY is not set, check if go module is running")
        return cls(secret)

    def _encode(self, data: dict) -> str:
        return jwt.encode(data, self.secret, algorithm="HS256")
    
    def _decode(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=["HS256"])
    
    def _verify_token_data(self, data: dict) -> bool | str:
        # First check for fields
        if "ID" not in data or "exp" not in data or "iss" not in data:
            return False, "Invalid token data"
        # Then check for expiration time
        if data["exp"] < time.time():
            return False, "Expired Token"
        # Then check for issuer
        if data["iss"] != "aiLearn":
            return False, "Invalid issuer"
        return True, "Valid token data"
    
    def decode_token(self, token: str) -> dict:
        """
        Returns the decoded token if it is valid.
        Decoded should be: 
        {
            "ID": 123, # User ID (uint64)
            "exp": 1234567890, # Expiration time (unix timestamp)
            "iss": "aiLearn" # Standard Issuer
        }
        """
        try:
            data = self._decode(token)
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
        else:
            valid, msg = self._verify_token_data(data)
            if not valid:
                raise ValueError(msg)
            return data
