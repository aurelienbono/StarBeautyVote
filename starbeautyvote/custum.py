from datetime import datetime, timedelta
from starbeautyvote import models
from django.db.models import Sum , Q
import secrets
import os 
from django.utils import timezone


class Starbeautyvote : 
    def __init__(self) -> None:
        pass
    
    def generate_random_string(length=16):
        """
        Generates a random alphanumeric string of specified length.

        Args:
            length (int, optional): The desired length of the random string. Defaults to 10.

        Returns:
            str: A random alphanumeric string.
        """
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    def modify_filename(filename,image_name):
	    # Change the filename from a.jpg to ab.jpg
        new_filename = image_name + os.path.splitext(filename)[1]
        return new_filename

    def voteNumberToFinalAmount(votes) : 
        votes = int(votes)
        numberOfTranches = votes // 10
        resteOfVote = votes % 10
        finalAmout = (numberOfTranches * 11 * 100) + (resteOfVote * 100)
        
        return finalAmout


    def percentageCalculate(totalOfLastWeek , totalOfCurrentWeek): 
        
        if totalOfLastWeek == 0:
            
            if totalOfCurrentWeek == 0:
                percentageChange = 0
                status = 'up'  # Both weeks have 0, no change
            else:
                percentageChange = 100  # Change from 0 to a positive number is 100%
                status = 'up'
            return percentageChange, status
        else : 
            change = totalOfCurrentWeek - totalOfLastWeek 
            percentageChange = (change/totalOfLastWeek) * 100 
            
            if totalOfLastWeek > totalOfCurrentWeek:
                status = 'up'
            else:
                 status = 'down'
                 
            return percentageChange , status




    def get_total_performance_for_week(pk , typeOfAggr, perfomance_type='candidate', week='current'):

        today = timezone.now()
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

        value = 0
        
        if perfomance_type=='candidate': 
            
            if typeOfAggr == "total_price"   : 
                
                value = models.Votes.objects.filter(
                    id_candidates=pk,
                    dataOfVoting__range=(start_date, end_date)
                ).aggregate(total_price=Sum('priceVoter'))['total_price']
            

            if typeOfAggr == "total_votes" : 
                
                value = models.Votes.objects.filter(
                    id_candidates=pk,
                    dataOfVoting__range=(start_date, end_date)
                ).aggregate(total_votes=Sum('numberOfVote'))['total_votes']
                
        else : 
            if typeOfAggr == "total_price"   : 
                
                value = models.Votes.objects.filter(
                    id_competition=pk,
                    dataOfVoting__range=(start_date, end_date)
                ).aggregate(total_price=Sum('priceVoter'))['total_price']
            

            if typeOfAggr == "total_votes" : 
                
                value = models.Votes.objects.filter(
                    id_competition=pk,
                    dataOfVoting__range=(start_date, end_date)
                ).aggregate(total_votes=Sum('numberOfVote'))['total_votes']            
                
                
            
        if value is  None : 
            return 0 
        else : 
            return value
        
    def get_total_performance_of_candidate_for_week(pk , week='current'):
        
        today = timezone.now()
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
        
        value = models.Candidates.objects.filter(id_competition = pk , 
                                                 dataOfRegistration__range = (start_date,end_date)
                                                 ).values().count()
        
        
        if value is  None : 
            return 0 
        else : 
            return value
        
    
    
    def get_total_of_amount_promoter(id_promoter_instance): 
        
        competition_ids = models.Competition.objects.filter(id_promoter=id_promoter_instance).values_list('competitionId', flat=True)

        competition_ids_list = list(competition_ids)
        sum_total_price = 0
        
        for elt in competition_ids_list : 
            total_price = models.Votes.objects.filter(
                       Q(id_competition=elt) & (Q(vote_type='public_paid') | Q(vote_type='promoter_paid'))
                ).aggregate(total_price=Sum('priceVoter'))['total_price']
            sum_total_price+= total_price
        
        return sum_total_price
    
    
    
    def get_competition_info_promoter(self, id_promoter_instance): 
    
        competition_ids = models.Competition.objects.filter(id_promoter=id_promoter_instance).values_list('competitionId', flat=True)
        competition_ids_list = list(competition_ids)
        competition_details = []
        sum_total_price = 0
        
        for elt in competition_ids_list : 
            competition      = models.Votes.objects.filter(id_competition=elt)
            total_price      = competition.aggregate(total_price=Sum('priceVoter'))['total_price']
            total_votes      = competition.aggregate(total_votes=Sum('numberOfVote'))['total_votes']
            
            total_reel_price = models.Votes.objects.filter(
                       Q(id_competition=elt) & (Q(vote_type='public_paid') | Q(vote_type='promoter_paid'))
                ).aggregate(total_price=Sum('priceVoter'))['total_price']
            
            total_reel_votes = models.Votes.objects.filter(
                       Q(id_competition=elt) & (Q(vote_type='public_paid') | Q(vote_type='promoter_paid'))
                ).aggregate(total_votes=Sum('numberOfVote'))['total_votes']
            
            competition_details.append({
                'competition': elt,
                'votes': total_votes,
                'total_price': total_price, 
                'total_reel_votes': total_reel_votes,
                'total_reel_price': total_reel_price
            })
        
        return competition_details