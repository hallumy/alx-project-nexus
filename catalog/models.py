from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Represents a product category with an optional parent category.
    Supports hierarchical organization through self-referencing.
    """
    name          = models.CharField(max_length=45)
    description   = models.TextField(blank=True, null=True)
    parent_id     = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', 
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    """
    Represents a product with pricing, stock, and category assignment.
    Supports optional descriptions, images, and brand details.
    """
    category       = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    name           = models.CharField(max_length=45)
    description    = models.TextField(blank=True, null=True)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    sku            = models.CharField(max_length=80)
    date_added     = models.DateTimeField(auto_now=True)
    is_active      = models.BooleanField()
    image_url      = models.ImageField(upload_to='product/', blank=True, null=True)
    brand          = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name} - {self.price}"
    

class Variant(models.Model):
    """
    Represents a purchasable variant of a product, such as size or color.
    Stores its own price, stock, SKU, and optional image
    """
    product       = models.ForeignKey('Product', on_delete=models.CASCADE)
    variant_name  = models.CharField(max_length=45)
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    stock         = models.IntegerField()
    sku           = models.CharField(max_length=80)
    image_url     = models.ImageField(upload_to='product/', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"

class Inventory(models.Model):
    """
    Tracks current stock quantities for product variants.
    Updates automatically whenever inventory changes occur.
    """
    variant       = models.ForeignKey('Variant', on_delete=models.CASCADE)
    quantity      = models.IntegerField()
    updated_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inventory for {self.variant.variant_name}: {self.quantity}"

class Discount(models.Model):
    """
    Represents a discount rule that applies within a date range.
    Supports percentage or fixed amount discounts with conditions.
    """
    code             = models.CharField(max_length=20)
    description      = models.CharField(max_length=225)
    discount_type    = models.CharField(max_length=20)
    minimum_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date       = models.DateTimeField(auto_now=True)
    end_date         = models.DateTimeField(auto_now=True)
    is_active        = models.BooleanField()

    def __str__(self):
        return f"Discount {self.code}"


class ProductDiscount(models.Model):
    """
    Links a discount to a specific product.
    Allows multiple discounts to be applied across products.
    """
    discount    = models.ForeignKey('Discount', on_delete=models.CASCADE)
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.discount.code} -> {self.product.name}"    


class Wishlist(models.Model):
    """
    Stores products a user is interested in saving for later.
    Each wishlist is tied to a single user.
    """
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user}"


class WishlistItem(models.Model):
    """
    Represents a product saved inside a wishlist.
    Each item links a wishlist with a specific product.
    """
    wishlist = models.ForeignKey('Wishlist', on_delete=models.CASCADE)
    product  = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in wishlist {self.wishlist.id}"

class Cart(models.Model):
    """
    Represents a user's shopping cart, storing selected products and their quantities.
    Allows users to accumulate items before proceeding to checkout.
    """
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user}"
    
class CartItem(models.Model):
    """
    Represents an individual product added to a user's cart, including the
    selected quantity and a reference to the related cart and product.
    """
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True)
    variant     = models.ForeignKey('Variant', on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.variant.variant_name} x {self.quantity}"