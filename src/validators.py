from re import search
from django.core.exceptions import ValidationError

class authenticationValidators:

    def passwordValid(password):
        if not search(".{8}", password):

            return "Password must be at least 8 characters long"
        
        if search(".{17,}", password):

            return "Password cannot exceed 16 characters"
        
        if not search("[a-z]", password):

            return "Password must have at least one lowercase letter"
        
        if not search("[A-Z]", password):

            return "Password must have at least one uppercase letter"
        
        if not search("[0-9]", password):

            return "Password must have at least one digit"
        
        if not search(".*[\¬\!\"\£\$\%\^\&\*\(\)\_\+\`\-\=\{\}\:\@\~\<\>\?\[\]\;\'\#\,\.\/\\\|]", password):

            return "Password must have at least one special character"