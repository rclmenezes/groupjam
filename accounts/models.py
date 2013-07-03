from django.db import models

class RegistrationManager(models.Model):
    id = models.AutoField(primary_key=True)
    confirmation_code = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    
    def confirmation_url(self):
        return '/register/email_confirm/?confirmation_code=' + self.confirmation_code