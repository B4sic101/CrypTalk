from re import search
from django.core.exceptions import ValidationError

class authenticationValidators:


    '''
    if myUser.objects.filter(email=request.POST["email"]).exists():
        error = "An account with this email already exists.
    
    '''
    '''
    
    if re.search("^\s|\s{2,}|\s$", request.POST["username"]):
    '''

    def passwordValid(self, password):
        if not search("^(?=.*\d)", password):
            raise ValidationError(
                "Password must have atleast one digit",
                code="password_no_digit"
            )
        if not search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$", password):
            raise ValidationError(
                "Password invalid, for valid: 8 characters minimum, one lowercase & uppercase letter, one number, and one special character.",
                code="password_invalid"
            )