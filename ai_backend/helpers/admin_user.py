from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

# Permission helpers (Admins should access user and admin routes)
def user_required(fn):
   @wraps
   def wrapper(*args, **kwargs):
      claims = get_jwt()

      if claims.get("role") not in ["user", "admin"]:
         return {"error": "Access denied"}, 403
      
      return fn(*args, **kwargs)
   return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({"error": "Admins only"}), 403

        return fn(*args, **kwargs)

    return wrapper

from functools import wraps

def preserve_docs(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper