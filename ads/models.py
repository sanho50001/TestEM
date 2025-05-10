from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('like_new', 'Как новый'),
        ('good', 'Хорошее'),
        ('satisfactory', 'Удовлетворительное'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('completed', 'Завершено'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_proposals')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_proposals')
    offered_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='offered_in_proposals')
    desired_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='desired_in_proposals')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Обмен {self.offered_item.title} на {self.desired_item.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Профиль {self.user.username}"
