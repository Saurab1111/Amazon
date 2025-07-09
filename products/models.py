from django.db import models
from django.utils.text import slugify
class Product(models.Model):
    name= models.CharField(max_length=100)
    description=models.CharField(max_length=2000)
    slug=models.SlugField(   #slug is just inheritance of CharField hence default is ""
        max_length=200,
        unique=True,
        blank=True,
    )
    price=models.IntegerField()
    is_available= models.BooleanField()
    quantity_available= models.IntegerField()
    product_image=models.URLField()
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        else:
            base_slug=slugify(self.name)
            count=0
            while Product.objects.filter(slug=base_slug).exists():
                count+=1
                base_slug+=f'-count'
            self.slug=base_slug
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name