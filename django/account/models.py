from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


#カスタムユーザーモデルを作成
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, familygroup=familygroup, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


#FamilyGroupsテーブルの設定
class FamilyGroup(models.Model):
    class Meta:
        db_table = 'FamilyGroups'

    name = models.CharField(verbose_name="グループ名", max_length=50, unique=True, null=False)
    password = models.CharField(verbose_name="合言葉", max_length=100, null=False)
    create_at = models.DateTimeField(verbose_name="登録日", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="更新日時", default=timezone.now)

    def __str__(self):
        return self.name


#Usersテーブルの設定
class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'Users'

    name = models.CharField(verbose_name="ユーザー名", max_length=50)
    email = models.EmailField(verbose_name="メールアドレス", max_length=254, unique=True)
    create_at = models.DateTimeField(verbose_name="登録日", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="更新日時", default=timezone.now)

    familygroup = models.ForeignKey(FamilyGroup, verbose_name="グループID",  on_delete=models.CASCADE)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #AbstractBaseUserに必要
    objects = CustomUserManager()

    #一意の識別子として使用する
    USERNAME_FIELD = "email"
    #サインアップ時に必須のフィールド
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email