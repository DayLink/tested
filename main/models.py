from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)
from sorl.thumbnail import ImageField
from sorl.thumbnail import get_thumbnail
from tinymce.models import HTMLField




class Category(models.Model):
    title = models.CharField(max_length=200, unique=True, )
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=200, unique=True, )
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to='uploads/post/', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title

    def preview(self):
        if self.image:
            im = get_thumbnail(self.image, '100x100', crop='center')
            return '<img src="%s">' % im.url
        return ''

    preview.allow_tags = True

    @models.permalink
    def get_absolute_url(self):
        return ('view_post', (), {
            'category_slug': self.category.slug,
            'post_slug': self.slug,
    })

class Comment(models.Model):
    post = models.ForeignKey(Post)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()


class MyUserManager(BaseUserManager):
    def create_user(self, username, name, gender, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username address')

        user = self.model(username=username,
            name=name,
            gender=gender,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, gender, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username=username,
            name=name,
            gender=gender,
            email=self.normalize_email(email),
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=(('M','Male'),('F','Female')))
    avatar = ImageField(upload_to='avatar/%Y/%m/%d', blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','date_of_birth','email','gender']

    def get_full_name(self):
        # The user is identified by their username address
        return self.username

    def get_short_name(self):
        # The user is identified by their username address
        return self.username

    def __unicode__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def preview_avatar(self):
        if self.avatar:
            im = get_thumbnail(self.avatar, '100x100', crop='center')
            return '<img src="%s">' % im.url
        return ''

    preview_avatar.allow_tags = True

