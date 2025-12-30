from django import forms
from .models import Trade, TradeImage, Strategy

class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['name', 'description']

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['symbol', 'trade_type', 'entry_date', 'entry_price', 'quantity', 'stop_loss', 'target', 'strategy', 'emotion', 'is_backtest', 'notes', 'status', 'exit_price', 'exit_date']
        widgets = {
            'entry_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'exit_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
        strategies = Strategy.objects.filter(user=user)
        self.fields['strategy'].queryset = strategies
        
        # If no strategies exist, create default ones
        if not strategies.exists():
            default_strategies = [
                {'name': 'Swing Trading', 'description': 'Medium-term trading strategy'},
                {'name': 'Day Trading', 'description': 'Short-term intraday trading'},
                {'name': 'Scalping', 'description': 'Very short-term trading'},
                {'name': 'Position Trading', 'description': 'Long-term trading strategy'},
            ]
            
            for strategy_data in default_strategies:
                Strategy.objects.create(user=user, **strategy_data)
            
            # Refresh queryset
            self.fields['strategy'].queryset = Strategy.objects.filter(user=user)

class TradeImageForm(forms.ModelForm):
    class Meta:
        model = TradeImage
        fields = ['image', 'caption']
