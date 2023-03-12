from django.db import models

# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True,related_name='+')

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField() 


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(default='-')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion,related_name='products')


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name','first_name'])
        ]


class Order(models.Model):
    PAYMENTSTATUS_PENDING = 'P'
    PAYMENTSTATUS_COMPLETE = 'C'
    PAYMENTSTATUS_FAILED = 'F'

    PAYMENT_STATUS = [
        (PAYMENTSTATUS_PENDING, 'Pending'),
        (PAYMENTSTATUS_COMPLETE, 'Complete'),
        (PAYMENTSTATUS_FAILED, 'Failed')
    ]

    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, default='P')

    placed_at = models.DateTimeField(auto_now_add=True)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)
    zipcode = models.PositiveIntegerField(null=True)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
