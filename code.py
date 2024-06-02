from starbeautyvote import models
from datetime import datetime, timedelta
from django.db.models import Sum



def get_total_price_for_week(pk, week='current'):
        today = datetime.now()
        start_of_current_week = today - timedelta(days=today.weekday())
        start_of_last_week = start_of_current_week - timedelta(days=7)
        end_of_last_week = start_of_current_week - timedelta(seconds=1)


        if week == 'current':
            start_date = start_of_current_week
            end_date = today

        elif week == 'last':
            start_date = start_of_last_week
            end_date = end_of_last_week
        
        else:
            raise ValueError("Invalid week parameter. Use 'current' or 'last'.")

        total_price = models.Votes.objects.filter(
            id_candidates=pk,
            dataOfVoting=[start_date, end_date]
        ).aggregate(total_price=Sum('priceVoter'))['total_price']

        return total_price

    # # Utilisation pour la semaine en cours
    # context['total_price_current_week'] = get_total_price_for_week(pk, week='current')

    # # Utilisation pour la semaine précédente
    # context['total_price_last_week'] = get_total_price_for_week(pk, week='last')

