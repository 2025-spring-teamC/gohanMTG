from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


#カスタムユーザーマネージャー
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None, familygroup=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です")
        if not password:
            raise ValueError("パスワードは必須です")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, familygroup=familygroup, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name=None, password=None, familygroup=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, name=name, familygroup=familygroup, **extra_fields)


#FamilyGroupsテーブルの設定
class FamilyGroup(models.Model):

    name = models.CharField(verbose_name="グループ名", max_length=20, null=False)
    password = models.CharField(verbose_name="合言葉", max_length=255, null=False)
    created_at = models.DateTimeField(verbose_name="登録日", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        db_table = "FamilyGroups"
        constraints = [
            models.UniqueConstraint(fields=["name", "password"], name="unique_name_password")
        ]

    def __str__(self):
        return self.name


#Usersテーブルの設定
class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "Users"

    name = models.CharField(verbose_name="ユーザー名", max_length=50, null=False, blank=False)
    email = models.EmailField(verbose_name="メールアドレス", max_length=254, null=False, unique=True)
    created_at = models.DateTimeField(verbose_name="登録日", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    familygroup = models.ForeignKey(
        FamilyGroup,
        verbose_name="所属グループ",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    #一意の識別子として使用する
    USERNAME_FIELD = "email"
    #サインアップ時に必須のフィールド
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.email})"