from django.core.management.base import BaseCommand
from portfolio.models import Portfolio

class Command(BaseCommand):
    help = 'Recalculate all portfolio balances'

    def handle(self, *args, **options):
        portfolios = Portfolio.objects.all()
        count = 0
        
        self.stdout.write(self.style.WARNING(f'Recalculating {portfolios.count()} portfolios...'))
        
        for portfolio in portfolios:
            old_balance = portfolio.current_balance
            new_balance = portfolio.calculate_balance()
            
            if old_balance != new_balance:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated {portfolio.user.username}: Rs.{old_balance} -> Rs.{new_balance}'
                    )
                )
            count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} portfolios'))
