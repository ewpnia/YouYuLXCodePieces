# Base Models

from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

class BaseModel(models.Model):
    uid = models.AutoField(max_length=32, primary_key=True)

    class Meta:
        abstract = True
        ordering = ["uid"]


class NameMixin(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        abstract = True
        ordering = ["uid"]


class DescriptionMixin(models.Model):
    description = models.TextField(default='None')

    class Meta:
        abstract = True
        ordering = ["uid"]


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["uid"]


class BooleanMixin(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ["uid"]


class Entity(BaseModel):
    class Meta:
        abstract = True
        ordering = ["uid"]


class Relationship(BaseModel):
    class Meta:
        abstract = True
        ordering = ["uid"]


# Please note that if you are using multi-inheritance, 
# MPTTModel should usually be the first class to be inherited from.
# If MPTTModel is not the first Model, 
# you may get errors at Model validation, 
# like AttributeError: 'NoneType' object has no attribute 'name'.
class BaseTreeModel(MPTTModel):
    uid = models.AutoField(max_length=32, primary_key=True)
    parent = TreeForeignKey('self', null = True, blank = True,\
               related_name = 'children', db_index = True)

    class Meta:
        abstract = True
        ordering = ["uid"]

