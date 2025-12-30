from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trade, TradeImage, Strategy
from .forms import TradeForm, TradeImageForm, StrategyForm

@login_required
def trade_list(request):
    trades = Trade.objects.filter(user=request.user).order_by('-entry_date')
    return render(request, 'journal/trade_list.html', {'trades': trades})

@login_required
def trade_create(request):
    if request.method == 'POST':
        form = TradeForm(request.user, request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user
            trade.save()
            messages.success(request, 'Trade logged successfully!')
            return redirect('trade_list')
    else:
        form = TradeForm(request.user)
    return render(request, 'journal/trade_form.html', {'form': form, 'title': 'Log New Trade'})

@login_required
def trade_detail(request, pk):
    trade = get_object_or_404(Trade, pk=pk, user=request.user)
    return render(request, 'journal/trade_detail.html', {'trade': trade})

@login_required
def trade_update(request, pk):
    trade = get_object_or_404(Trade, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TradeForm(request.user, request.POST, instance=trade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trade updated successfully!')
            return redirect('trade_detail', pk=pk)
    else:
        form = TradeForm(request.user, instance=trade)
    return render(request, 'journal/trade_form.html', {'form': form, 'title': 'Update Trade'})

@login_required
def trade_delete(request, pk):
    trade = get_object_or_404(Trade, pk=pk, user=request.user)
    if request.method == 'POST':
        trade.delete()
        messages.success(request, 'Trade deleted successfully!')
        return redirect('trade_list')
    return render(request, 'journal/trade_confirm_delete.html', {'trade': trade})

@login_required
def strategy_list(request):
    strategies = Strategy.objects.filter(user=request.user)
    return render(request, 'journal/strategy_list.html', {'strategies': strategies})

@login_required
def strategy_create(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            strategy = form.save(commit=False)
            strategy.user = request.user
            strategy.save()
            messages.success(request, 'Strategy created successfully!')
            return redirect('strategy_list')
    else:
        form = StrategyForm()
    return render(request, 'journal/strategy_form.html', {'form': form, 'title': 'Create New Strategy'})
