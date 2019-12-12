# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TCommodity(models.Model):
    commodity_id = models.CharField(primary_key=True, max_length=20)
    merchant_id = models.CharField(max_length=20)
    price = models.FloatField()
    category_id = models.CharField(max_length=20, blank=True, null=True)
    commodity_category = models.CharField(max_length=20)
    brand_id = models.CharField(max_length=20, blank=True, null=True)
    commodity_brand = models.CharField(max_length=20)
    commodity_doc = models.CharField(max_length=200, blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_commodity'


class TLoginUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_login_user'


class TMerchant(models.Model):
    merchant_id = models.CharField(primary_key=True, max_length=20)
    gmv = models.CharField(db_column='GMV', max_length=50, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_merchant'


class TUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    preference = models.CharField(max_length=50, blank=True, null=True)
    consume_level = models.CharField(max_length=20, blank=True, null=True)
    consume_frequency = models.CharField(max_length=20, blank=True, null=True)
    area_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'


class TUserAddToCart(models.Model):
    user_id = models.CharField(max_length=20, blank=True, null=True)
    commodity_id = models.CharField(max_length=20, blank=True, null=True)
    time_stamp = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user_add_to_cart'


class TUserAddToFavorite(models.Model):
    user_id = models.CharField(max_length=20, blank=True, null=True)
    commodity_id = models.CharField(max_length=20, blank=True, null=True)
    time_stamp = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user_add_to_favorite'


class TUserClick(models.Model):
    user_id = models.CharField(max_length=20, blank=True, null=True)
    commodity_id = models.CharField(max_length=20, blank=True, null=True)
    time_stamp = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user_click'


class TUserPurchase(models.Model):
    user_id = models.CharField(max_length=20, blank=True, null=True)
    commodity_id = models.CharField(max_length=20, blank=True, null=True)
    time_stamp = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user_purchase'


class TGenderDistribute(models.Model):
    merchant_id = models.CharField(max_length=20, blank=True, null=False)
    gender = models.CharField(max_length=20, blank=True, null=True)
    count = models.CharField(max_length=21, blank=True, null=False,default=0)

    class Meta:
        managed = False
        db_table = 't_gender_distribute'
