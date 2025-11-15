from django.db import models


class Category(models.Model):
    """
    Represents a product category, which can have a name, description,
    and optional parent category. Supports hierarchical relationships
    with subcategories through the parent field.
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
    Represents a product in the e-commerce system, including its name, price, 
    category, and optional image.Supports linking to a category and storing 
    either a local image or external image URL.
    """
    category       = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product')
    name           = models.CharField(max_length=45)
    description    = models.TextField(blank=True, null=True)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    sku            = models.CharField(max_lenght=80)
    date_added     = models.DateTimeField(auto_now=True)
    is_active      = models.BooleanField()
    image_url      = models.ImageField(upload_to='product/', blank=True, null=True)
    brand          = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name} - {self.price}"
    

class Variant(models.Model):
    """ 
    """
    product       = models.ForeignKey('Product', on_delete=models.CASCADE)
    variant_name  = models.CharField(max_length=45)
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    stock         = models.IntegerField()
    sku           = models.CharField(max_lenght=80)
    image_url     = models.ImageField(upload_to='product/', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=True)