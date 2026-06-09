from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('investor', 'Investor'),
        ('entrepreneur', 'Entrepreneur'),
    )

    STAGE_CHOICES = (
        ('idea', 'Idea Stage'),
        ('mvp', 'MVP'),
        ('early', 'Early Revenue'),
        ('growth', 'Growth Stage'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=120)
    headline = models.CharField(max_length=160, blank=True)
    company_name = models.CharField(max_length=120, blank=True)
    industry = models.CharField(max_length=100)
    city = models.CharField(max_length=80, blank=True)
    bio = models.TextField()
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, blank=True)
    funding_need = models.CharField(max_length=100, blank=True)
    ticket_size = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    verified = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class StartupPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    content = models.TextField()
    funding_goal = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=80, blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Connection(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f'{self.sender} -> {self.receiver} ({self.status})'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} to {self.receiver}'


class ContactReveal(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_reveals')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revealed_to')
    accepted_terms = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    revealed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('viewer', 'target')
