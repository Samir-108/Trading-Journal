from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from .models import Portfolio, Transaction
from .forms import PortfolioForm, TransactionForm
from datetime import datetime, timedelta
import json

@login_required
def portfolio_dashboard(request):
    try:
        portfolio = request.user.portfolio
    except Portfolio.DoesNotExist:
        # Auto-create portfolio if it doesn't exist
        portfolio = Portfolio.objects.create(user=request.user)
    
    # Get all transactions
    all_transactions = portfolio.transactions.order_by('date')
    recent_transactions = all_transactions.order_by('-date')[:10]
    
    # Calculate deposits and withdrawals
    deposits = all_transactions.filter(transaction_type='DEPOSIT')
    withdrawals = all_transactions.filter(transaction_type='WITHDRAWAL')
    
    total_deposits = deposits.aggregate(Sum('amount'))['amount__sum'] or 0
    total_withdrawals = withdrawals.aggregate(Sum('amount'))['amount__sum'] or 0
    deposit_count = deposits.count()
    withdrawal_count = withdrawals.count()
    
    # Calculate balance history for chart
    balance_history = []
    balance_labels = []
    running_balance = float(portfolio.initial_capital)
    
    # Group transactions by date
    from collections import defaultdict
    daily_transactions = defaultdict(list)
    for txn in all_transactions:
        date_str = txn.date.strftime('%Y-%m-%d')
        daily_transactions[date_str].append(txn)
    
    # Get trades for P&L calculation
    closed_trades = request.user.trades.filter(status='CLOSED').order_by('exit_date')
    
    # Build balance history
    all_dates = set()
    for txn in all_transactions:
        all_dates.add(txn.date.date())
    for trade in closed_trades:
        if trade.exit_date:
            all_dates.add(trade.exit_date.date())
    
    all_dates = sorted(all_dates)
    
    if all_dates:
        for date in all_dates:
            date_str = date.strftime('%Y-%m-%d')
            
            # Add transaction amounts
            if date_str in daily_transactions:
                for txn in daily_transactions[date_str]:
                    if txn.transaction_type == 'DEPOSIT':
                        running_balance += float(txn.amount)
                    else:
                        running_balance -= float(txn.amount)
            
            # Add trade P&L
            for trade in closed_trades:
                if trade.exit_date and trade.exit_date.date() == date:
                    if trade.pnl:
                        running_balance += float(trade.pnl)
            
            balance_labels.append(date.strftime('%b %d'))
            balance_history.append(round(running_balance, 2))
    else:
        # No transactions yet, just show initial capital
        balance_labels = ['Start']
        balance_history = [float(portfolio.initial_capital)]
    
    # Calculate net profit/loss manually (since pnl is a property, not a field)
    total_pnl = 0
    for trade in closed_trades:
        if trade.pnl:
            total_pnl += float(trade.pnl)
    
    net_change = float(portfolio.current_balance) - float(portfolio.initial_capital)
    
    # Calculate transaction balance after for each recent transaction
    transactions_with_balance = []
    temp_balance = float(portfolio.current_balance)
    for txn in recent_transactions:
        transactions_with_balance.append({
            'transaction': txn,
            'balance_after': temp_balance
        })
        # Reverse calculate (going backwards in time)
        if txn.transaction_type == 'DEPOSIT':
            temp_balance -= float(txn.amount)
        else:
            temp_balance += float(txn.amount)
    
    context = {
        'portfolio': portfolio,
        'transactions': transactions_with_balance,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'deposit_count': deposit_count,
        'withdrawal_count': withdrawal_count,
        'balance_labels': json.dumps(balance_labels),
        'balance_history': json.dumps(balance_history),
        'total_pnl': total_pnl,
        'net_change': net_change,
        'net_change_percent': (net_change / float(portfolio.initial_capital) * 100) if portfolio.initial_capital > 0 else 0,
    }
    return render(request, 'portfolio/dashboard.html', context)

@login_required
def update_portfolio(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Portfolio settings updated!')
            return redirect('portfolio_dashboard')
    else:
        form = PortfolioForm(instance=portfolio)
    return render(request, 'portfolio/portfolio_form.html', {'form': form})

@login_required
def add_transaction(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.portfolio = portfolio
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('portfolio_dashboard')
    else:
        form = TransactionForm()
    return render(request, 'portfolio/transaction_form.html', {'form': form})
