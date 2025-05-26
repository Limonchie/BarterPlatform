from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request, "Объявление успешно создано!")
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})


def ad_list(request):
    ads_list = Ad.objects.all().order_by('-created_at')

    category = request.GET.get('category')
    if category:
        ads_list = ads_list.filter(category=category)

    search_query = request.GET.get('search')
    if search_query:
        ads_list = ads_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(ads_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {
        'page_obj': page_obj,
        'category_choices': Ad.CATEGORY_CHOICES
    })


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if not ad.user == request.user:
        messages.error(request, "У вас нет прав на редактирование этого объявления")
        return redirect('ad_list')

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, "Объявление успешно обновлено!")
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/edit_ad.html', {'form': ad, 'ad': ad})


@login_required
def delete_ad(request, ad_id):
    """Удаление объявления"""
    ad = get_object_or_404(Ad, id=ad_id)

    if not ad.user == request.user:
        messages.error(request, "У вас нет прав на удаление этого объявления")
        return redirect('ad_list')

    if request.method == 'POST':
        ad.delete()
        messages.success(request, "Объявление успешно удалено!")
        return redirect('ad_list')

    return render(request, 'ads/delete_confirm.html', {'ad': ad})


@login_required
def create_proposal(request, ad_sender_id):
    """Создание предложения обмена"""
    ad_sender = get_object_or_404(Ad, id=ad_sender_id, user=request.user)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = ad_sender
            proposal.status = 'pending'
            proposal.save()
            messages.success(request, "Предложение обмена успешно отправлено!")
            return redirect('proposals_list')
    else:
        form = ExchangeProposalForm()

    return render(request, 'ads/create_proposal.html', {
        'form': form,
        'ad_sender': ad_sender
    })


@login_required
def proposals_list(request):
    """Список предложений обмена"""
    proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) |
        Q(ad_receiver__user=request.user)
    ).order_by('-created_at')

    # Фильтрация по статусу
    status_filter = request.GET.get('status')
    if status_filter:
        proposals = proposals.filter(status=status_filter)

    # Пагинация
    paginator = Paginator(proposals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/../templates/proposals/proposals_list.html', {
        'page_obj': page_obj,
        'status_choices': ExchangeProposal.STATUS_CHOICES
    })


@login_required
def update_proposal_status(request, proposal_id, new_status):
    """Обновление статуса предложения"""
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if not proposal.ad_receiver.user == request.user:
        messages.error(request, "У вас нет прав на изменение этого предложения")
        return redirect('proposals_list')

    if new_status not in ['accepted', 'rejected']:
        messages.error(request, "Недопустимый статус")
        return redirect('proposals_list')

    proposal.status = new_status
    proposal.save()
    messages.success(request, f"Статус предложения изменен на {new_status}!")
    return redirect('proposals_list')