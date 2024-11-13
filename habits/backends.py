from django.contrib.auth import get_user_model
from django.db.models import Q # used to do OR queries in the database

# This backend provides the user with the ability to use either their username OR their email when logging on

class EmailOrUsernameBackend:
    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.filter(Q(username=username) | Q(email=username)).first() # Finds the user where either username OR email matches input from username field       
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
