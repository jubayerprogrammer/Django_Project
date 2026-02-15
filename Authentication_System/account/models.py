from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password
        """
        if not email:
            raise ValueError("User must have a valid email address")
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("SuperUser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser must have is_superuser=True.")

        # Create the user
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = False
        user.is_customer = True
        user.is_seller = False
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return super().has_perm(perm,obj)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return super().has_module_perms(app_label)
    


"""  

from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.

class User_manager(BaseUserManager):
    def create_User(self,email,password= None):
        #creates and saves an User with the given  email and password
        if not email:
            raise ValueError("User must have an valid email address")
        
        User = self.model(email= self.normalize_email(email))
        User.set_password(password)
        User.save(using= self._db)
        return User
    
    def create_superUser(self,email,password=None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superUser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError ("SuperUser must have is_straff= True. ")    


        #Creates and save a superUser with the given email and password

        User = self.create_User(email,password)
        User.is_staff = True
        User.is_superUser = True
        User.is_customar = True
        User.is_seller = False

        User.save(using= self._db)
        return User


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superUser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    uptated_at = models.DateField(auto_now=True)


    USERNAME_FIELD= 'email'
    objects = User_manager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj= None):
        "Does the User have a specific permission?"
        #Only SuperUser have permision to access all data 
        return self.is_superUser

    def has_module_perms(self,app_label):
        "Does the User have permissions to view the app `app_lavel` "    

        return self.is_superUser

        

    
    



"""