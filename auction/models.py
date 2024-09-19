from django.utils.text import slugify

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=255, default="EMAIL")
    created = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['created']

class Bid(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.bid > self.listing.current_bid:
            self.listing.current_bid = self.bid
            self.listing.save()


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('Fashion', 'Fashion'),
        ('Electronics', 'Electronics'),
        ('Home & Garden', 'Home & Garden'),
        ('Toy & Games', 'Toy & Games'),
        ('Collectibles', 'Collectibles'),
        ('Sports & Outdoors', 'Sports & Outdoors'),
        ('Books & Magazines', 'Books & Magazines'),
        ('Automotives', 'Automotives'),
        ('Music & Entertainment', 'Music & Entertainment'),
        ('Art & Crafts', 'Art & Crafts'),
        ('Food & Beverages', 'Food & Beverages'),
        ('Pets', 'Pets'),
        ('Other', 'Other'),
    ]


    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    closing_date = models.DateTimeField()
    category = models.CharField(max_length=50 ,choices=CATEGORY_CHOICES)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    def place_bid(self, user, amount):
        if amount > self.current_bid:
            bid = Bid.objects.create(
                listing=self,
                bidder=user,
                bid=amount
            )
            self.current_bid = amount
            self.save()
            return bid
        return None
    
    def get_highest_bid(self):
        return self.bid_set.order_by('-bid').first()

    def get_bid_count(self):
        return self.bid_set.count()

    def get_all_bids(self):
        return self.bid_set.all().order_by('-bid')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Check if the generated slug already exists
            num = 1
            while Listing.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{num}"
                num += 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']

