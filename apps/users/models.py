from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from apps.utils.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if username is None:
            raise TypeError({"success": False, "detail": _("User should have a phone")})
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **kwargs):
        user = self.create_user(username=username, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    username = models.CharField(max_length=255, verbose_name=_('Username'), unique=True, db_index=True)
    phone = models.CharField(max_length=12, verbose_name=_('Phone number'), unique=True, db_index=True)
    email = models.EmailField(max_length=255, verbose_name=_('Email'), unique=True, db_index=True, null=True, blank=True)

    first_name = models.CharField(max_length=50, verbose_name=_('First name'), null=True)
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'), null=True)
    middle_name = models.CharField(max_length=50, verbose_name=_('Last name'), null=True)

    is_superuser = models.BooleanField(default=False, verbose_name=_('Super user'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff user'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active user'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Verified user'))

    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))


class UserResetToken(models.Model):
    """
    A model that stores SMS codes sent to a user's number.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_id = models.CharField(max_length=255)
    content = models.TextField(editable=False)
    expire_date = models.DateTimeField(db_index=True)
    is_used = models.BooleanField(default=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone

    @property
    def full_name(self):
        return self.user.full_name

    @property
    def phone(self):
        return self.user.phone
