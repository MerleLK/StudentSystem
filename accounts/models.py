from django.db import models

# Create your models here.


# a user model
# copy by https://python-ning.github.io/2015/12/24/python_django_user_login_register_logout/
class User(models.Model):

    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=50)
    email = models.EmailField(null=False)
    datetime = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=30)
    image = models.ImageField(null=False, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username
