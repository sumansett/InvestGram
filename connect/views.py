from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Profile, StartupPost, Connection, Message, ContactReveal

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def home(request):
    posts = StartupPost.objects.select_related('author')[:6]
    investors = Profile.objects.filter(role='investor')[:4]
    startups = Profile.objects.filter(role='entrepreneur')[:4]
    return render(request, 'connect/home.html', {
        'posts': posts,
        'investors': investors,
        'startups': startups,
    })

def explore(request):
    q = request.GET.get('q', '')
    role = request.GET.get('role', '')
    profiles = Profile.objects.select_related('user').all()

    if q:
        profiles = profiles.filter(
            Q(full_name__icontains=q) |
            Q(company_name__icontains=q) |
            Q(industry__icontains=q) |
            Q(city__icontains=q)
        )
    if role:
        profiles = profiles.filter(role=role)

    return render(request, 'connect/explore.html', {'profiles': profiles, 'q': q, 'role': role})

@login_required
def dashboard(request):
    profile = Profile.objects.filter(user=request.user).first()
    pending = Connection.objects.filter(receiver=request.user, status='pending').count()
    accepted = Connection.objects.filter(Q(sender=request.user) | Q(receiver=request.user), status='accepted').count()
    unread = Message.objects.filter(receiver=request.user, is_read=False).count()
    posts = StartupPost.objects.filter(author=request.user)
    return render(request, 'connect/dashboard.html', {
        'profile': profile,
        'pending': pending,
        'accepted': accepted,
        'unread': unread,
        'posts': posts,
    })

def profile_detail(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    posts = StartupPost.objects.filter(author=profile.user)
    connection = None
    revealed = False
    if request.user.is_authenticated:
        connection = Connection.objects.filter(
            Q(sender=request.user, receiver=profile.user) |
            Q(sender=profile.user, receiver=request.user)
        ).first()
        revealed = ContactReveal.objects.filter(viewer=request.user, target=profile.user).exists()
    return render(request, 'connect/profile_detail.html', {
        'profile': profile,
        'posts': posts,
        'connection': connection,
        'revealed': revealed,
    })

@login_required
def send_connection(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if receiver == request.user:
        messages.error(request, 'You cannot connect with yourself.')
        return redirect('explore')

    note = request.POST.get('note', '')
    Connection.objects.get_or_create(sender=request.user, receiver=receiver, defaults={'note': note})
    messages.success(request, 'Connection request sent.')
    return redirect('profile_detail', user_id=user_id)

@login_required
def connections(request):
    received = Connection.objects.filter(receiver=request.user).select_related('sender')
    sent = Connection.objects.filter(sender=request.user).select_related('receiver')
    return render(request, 'connect/connections.html', {'received': received, 'sent': sent})

@login_required
def respond_connection(request, connection_id, action):
    connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
    if action == 'accept':
        connection.status = 'accepted'
        messages.success(request, 'Connection accepted.')
    elif action == 'reject':
        connection.status = 'rejected'
        messages.info(request, 'Connection rejected.')
    connection.save()
    return redirect('connections')

@login_required
def inbox(request):
    contacts = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()
    return render(request, 'connect/inbox.html', {'contacts': contacts})

@login_required
def chat(request, user_id):
    other = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Message.objects.create(sender=request.user, receiver=other, body=body)
            messages.success(request, 'Message sent.')
            return redirect('chat', user_id=user_id)

    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other) | Q(sender=other, receiver=request.user)
    )
    chat_messages.filter(receiver=request.user).update(is_read=True)
    return render(request, 'connect/chat.html', {'other': other, 'chat_messages': chat_messages})

@login_required
def reveal_contact(request, user_id):
    target = get_object_or_404(User, id=user_id)
    ContactReveal.objects.get_or_create(
        viewer=request.user,
        target=target,
        defaults={'ip_address': get_client_ip(request), 'accepted_terms': True}
    )
    messages.success(request, 'Contact reveal recorded with anti-circumvention consent.')
    return redirect('profile_detail', user_id=user_id)

@login_required
def create_post(request):
    if request.method == 'POST':
        StartupPost.objects.create(
            author=request.user,
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            funding_goal=request.POST.get('funding_goal'),
            category=request.POST.get('category'),
        )
        messages.success(request, 'Pitch post created.')
        return redirect('dashboard')
    return render(request, 'connect/create_post.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        full_name = request.POST.get('full_name')
        industry = request.POST.get('industry')
        bio = request.POST.get('bio')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(
            user=user,
            role=role,
            full_name=full_name,
            industry=industry,
            bio=bio,
            headline=request.POST.get('headline', ''),
            company_name=request.POST.get('company_name', ''),
            city=request.POST.get('city', ''),
            funding_need=request.POST.get('funding_need', ''),
            ticket_size=request.POST.get('ticket_size', ''),
        )
        messages.success(request, 'Account created. Please login.')
        return redirect('login')
    return render(request, 'connect/register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'connect/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
