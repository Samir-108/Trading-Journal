from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Portfolio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolio')
    name = models.CharField(max_length=100, default='My Portfolio')
    initial_capital = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

    def calculate_balance(self):
        """Calculate and update current balance"""
        # Start with initial capital
        balance = self.initial_capital
        
        # Add deposits and subtract withdrawals
        transactions = self.transactions.all()
        for t in transactions:
            if t.transaction_type == 'DEPOSIT':
                balance += t.amount
            elif t.transaction_type == 'WITHDRAWAL':
                balance -= t.amount
                
        # Add realized PnL from closed trades
        trades = self.user.trades.filter(status='CLOSED')
        for trade in trades:
            if trade.pnl:
                balance += trade.pnl
                
        self.current_balance = balance
        self.save()
        return balance

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    )
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

# Signals to automatically update portfolio balance
@receiver(post_save, sender=Transaction)
def update_balance_on_transaction_save(sender, instance, created, **kwargs):
    """Update portfolio balance when a transaction is saved"""
    instance.portfolio.calculate_balance()

@receiver(post_delete, sender=Transaction)
def update_balance_on_transaction_delete(sender, instance, **kwargs):
    """Update portfolio balance when a transaction is deleted"""
    instance.portfolio.calculate_balance()

# Import Trade model and add signal for it
from journal.models import Trade

@receiver(post_save, sender=Trade)
def update_balance_on_trade_save(sender, instance, **kwargs):
    """Update portfolio balance when a trade is closed"""
    try:
        portfolio = instance.user.portfolio
        portfolio.calculate_balance()
    except Portfolio.DoesNotExist:
        pass

@receiver(post_delete, sender=Trade)
def update_balance_on_trade_delete(sender, instance, **kwargs):
    """Update portfolio balance when a trade is deleted"""
    try:
        portfolio = instance.user.portfolio
        portfolio.calculate_balance()
    except Portfolio.DoesNotExist:
        pass
