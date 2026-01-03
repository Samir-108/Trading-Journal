from django.db import models
from django.conf import settings
from django.utils import timezone

class Strategy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='strategies')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Trade(models.Model):
    TRADE_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    )
    EMOTION_CHOICES = (
        ('NEUTRAL', 'Neutral'),
        ('CONFIDENT', 'Confident'),
        ('ANXIOUS', 'Anxious'),
        ('GREEDY', 'Greedy'),
        ('FEARFUL', 'Fearful'),
        ('FOMO', 'FOMO'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trades')
    symbol = models.CharField(max_length=20)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    entry_date = models.DateTimeField(default=timezone.now)
    exit_date = models.DateTimeField(null=True, blank=True)
    
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Changed from CharField to ForeignKey
    strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True, blank=True, related_name='trades')
    
    emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES, default='NEUTRAL')
    is_backtest = models.BooleanField(default=False, help_text="Check if this is a backtest/paper trade")
    
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='OPEN')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    trade_reason = models.TextField(
    blank=True, 
    help_text="Why did you take this trade position?"
)


    def __str__(self):
        return f"{self.symbol} - {self.trade_type} ({self.entry_date.date()})"

    @property
    def pnl(self):
        if self.exit_price and self.status == 'CLOSED':
            diff = self.exit_price - self.entry_price
            if self.trade_type == 'SELL':
                diff = -diff
            return diff * self.quantity
        return None

class TradeImage(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='trade_images/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.trade}"
    

    
