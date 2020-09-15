from django.core.management.base import BaseCommand, CommandError

import os
import ast
import json
import requests
from ipl.models import Schedule

ROOT=os.environ['ROOT_URL'].strip()

class Command(BaseCommand):

    def handle(self, *args, **options):
        matches = Schedule.objects.all()

        predicted_winners=ast.literal_eval(requests.get(f'{ROOT}/api/winner').json()['data'])
        
        for key, match in enumerate(matches):
            if key<=55:
                match.predicted_winner=predicted_winners[key]
                match.save()
            else:
                qualifier_winners=requests.get(f'{ROOT}/api/qualifiers').json()['data']
                qf_type=match.qualifier_type
                match.team1=qualifier_winners[qf_type]['winner']+' (Predicted)'
                match.team2=qualifier_winners[qf_type]['loser']+' (Predicted)'
                match.predicted_winner=qualifier_winners[qf_type]['winner']
                match.save()
