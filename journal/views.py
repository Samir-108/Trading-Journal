from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Trade, TradeImage, Strategy
from .forms import TradeForm, TradeImageForm, StrategyForm

@login_required
def trade_list(request):
    trades = Trade.objects.filter(user=request.user)
    
    # Handle sorting
    sort_by = request.GET.get('sort_by', 'entry_date')
    order = request.GET.get('order', 'desc')
    
    # Determine field to sort by
    if sort_by == 'symbol':
        sort_field = 'symbol'
    elif sort_by == 'status':
        sort_field = 'status'
    else:
        sort_field = '-entry_date'
    
    # Apply sort direction
    if sort_by in ['symbol', 'status']:
        if order == 'asc':
            trades = trades.order_by(sort_field)
        else:
            trades = trades.order_by(f'-{sort_field}')
    else:
        trades = trades.order_by(sort_field)
    
    # Calculate total P&L (sum all closed trades' P&L)
    total_pnl = sum(trade.pnl for trade in trades if trade.pnl is not None)
    
    # Calculate total investment (sum of entry_price * quantity for all trades)
    total_investment = sum(trade.entry_price * trade.quantity for trade in trades)
    
    # Calculate win rate (winning trades / closed trades)
    closed_trades = [trade for trade in trades if trade.status == 'CLOSED']
    winning_trades = [trade for trade in closed_trades if trade.pnl and trade.pnl > 0]
    win_rate = (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0
    
    # Find best performer (trade with highest P&L)
    best_performer = max((trade for trade in closed_trades if trade.pnl is not None), 
                          key=lambda t: t.pnl, default=None)
    
    # Get portfolio net worth
    portfolio = request.user.portfolio if hasattr(request.user, 'portfolio') else None
    net_worth = portfolio.current_balance if portfolio else 0
    
    # Pass context to template including current sort state
    context = {
        'trades': trades,
        'current_sort': sort_by,
        'current_order': order,
        'total_pnl': total_pnl,
        'net_worth': net_worth,
        'win_rate': win_rate,
        'best_performer': best_performer,
        'total_investment': total_investment,
    }
    return render(request, 'journal/trade_list.html', context)

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


@login_required
@require_http_methods(["POST"])
def upload_trade_chart(request, pk):
    """Upload chart/image for a trade"""
    trade = get_object_or_404(Trade, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TradeImageForm(request.POST, request.FILES)
        if form.is_valid():
            trade_image = form.save(commit=False)
            trade_image.trade = trade
            trade_image.save()
            return JsonResponse({
                'success': True,
                'message': 'Chart/Image uploaded successfully!',
                'image_id': trade_image.id,
                'image_url': trade_image.image.url
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Error uploading chart. Please try again.',
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def trade_images(request, pk):
    """Get all images for a trade"""
    trade = get_object_or_404(Trade, pk=pk, user=request.user)
    images = trade.images.all().order_by('-created_at')
    
    images_data = [{
        'id': img.id,
        'url': img.image.url,
        'caption': img.caption,
        'created_at': img.created_at.strftime('%b %d, %Y %I:%M %p')
    } for img in images]
    
    return JsonResponse({'images': images_data})


@login_required
@require_http_methods(["DELETE"])
def delete_trade_image(request, pk, img_id):
    """Delete a specific trade image"""
    trade = get_object_or_404(Trade, pk=pk, user=request.user)
    image = get_object_or_404(TradeImage, id=img_id, trade=trade)
    
    image.delete()
    return JsonResponse({'success': True, 'message': 'Image deleted successfully!'})

