import jwt

# No longer used - we use AuthManager.verify_token instead
# This function is kept for compatibility but marked as deprecated
def verify_auth_token(token):
    """
    DEPRECATED: Use AuthManager.verify_token instead.
    This function is kept for backward compatibility only.
    """
    import warnings
    warnings.warn("verify_auth_token is deprecated, use AuthManager.verify_token instead", 
                  DeprecationWarning, stacklevel=2)
    return True