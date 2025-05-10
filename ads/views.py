from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Item, Category, ExchangeProposal, UserProfile
from .forms import ItemForm, ExchangeProposalForm, UserProfileForm
from django.utils.translation import gettext as _

def home(request):
    categories = Category.objects.all()
    items = Item.objects.filter(is_active=True).order_by('-created_at')[:12]
    return render(request, 'ads/home.html', {
        'categories': categories,
        'items': items
    })

def item_list(request):
    category = request.GET.get('category')
    search = request.GET.get('search')
    items = Item.objects.filter(is_active=True)
    
    if category:
        items = items.filter(category__slug=category)
    if search:
        items = items.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    return render(request, 'ads/item_list.html', {
        'items': items,
        'categories': Category.objects.all()
    })

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk, is_active=True)
    return render(request, 'ads/item_detail.html', {
        'item': item
    })

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, _('Объявление успешно создано!'))
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'ads/item_form.html', {'form': form})

@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, _('Объявление успешно обновлено!'))
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'ads/item_form.html', {'form': form})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.is_active = False
        item.save()
        messages.success(request, _('Объявление успешно удалено!'))
        return redirect('home')
    return render(request, 'ads/item_confirm_delete.html', {'item': item})

@login_required
def create_exchange_proposal(request, item_pk):
    desired_item = get_object_or_404(Item, pk=item_pk, is_active=True)
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.sender = request.user
            proposal.receiver = desired_item.owner
            proposal.desired_item = desired_item
            proposal.save()
            messages.success(request, _('Предложение обмена отправлено!'))
            return redirect('item_detail', pk=desired_item.pk)
    else:
        form = ExchangeProposalForm()
    return render(request, 'ads/exchange_proposal_form.html', {
        'form': form,
        'desired_item': desired_item
    })

@login_required
def proposal_list(request):
    sent_proposals = ExchangeProposal.objects.filter(sender=request.user)
    received_proposals = ExchangeProposal.objects.filter(receiver=request.user)
    return render(request, 'ads/proposal_list.html', {
        'sent_proposals': sent_proposals,
        'received_proposals': received_proposals
    })

@login_required
def proposal_detail(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    if proposal.sender != request.user and proposal.receiver != request.user:
        messages.error(request, _('У вас нет доступа к этому предложению!'))
        return redirect('home')
    return render(request, 'ads/proposal_detail.html', {'proposal': proposal})

@login_required
def accept_proposal(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk, receiver=request.user)
    if proposal.status == 'pending':
        proposal.status = 'accepted'
        proposal.save()
        messages.success(request, _('Предложение обмена принято!'))
    return redirect('proposal_detail', pk=proposal.pk)

@login_required
def reject_proposal(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk, receiver=request.user)
    if proposal.status == 'pending':
        proposal.status = 'rejected'
        proposal.save()
        messages.success(request, _('Предложение обмена отклонено!'))
    return redirect('proposal_detail', pk=proposal.pk)

@login_required
def complete_exchange(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    
    if proposal.status == 'pending':
            proposal.status = 'accepted'
            proposal.save()
            messages.success(request, _('Предложение обмена принято!'))

    elif proposal.status == 'accepted' and (proposal.sender == request.user or proposal.receiver == request.user):
        try:
            proposal.status = 'completed'
            proposal.save() 
            # Меняем владельцев товаров
            offered_item = proposal.offered_item
            desired_item = proposal.desired_item

            offered_item.owner = proposal.receiver
            desired_item.owner = proposal.sender

            offered_item.save()
            desired_item.save()

            # Удаляем предложение
            proposal.delete()

            messages.success(request, _('Обмен успешно завершен!'))

        except Exception as e:
            print(request, _('Произошла ошибка: %s' % str(e)))
            messages.error(request, _('Произошла ошибка: %s' % str(e)))
            

    else:
        messages.error(request, _('Вы не можете завершить этот обмен.'))
    return redirect('item_detail', pk=proposal.receiver.id)

@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Профиль успешно обновлен!'))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    items = Item.objects.filter(owner=request.user)
    propolsals = ExchangeProposal.objects.filter(sender=request.user)

    return render(request, 'ads/profile.html', {
        'form': form,
        'profile': profile,
        'user_items': items,
        'user_proposals': propolsals

    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, _('Регистрация успешно завершена!'))
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
