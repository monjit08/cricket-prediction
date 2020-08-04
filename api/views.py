from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import pickle
import numpy as np

# Create your views here.

cols = ['runs', 'wickets', 'overs', 'runs_last_5', 'wickets_last_5', 'striker',
       'non-striker', 'bat_team_Chennai Super Kings',
       'bat_team_Delhi Daredevils', 'bat_team_Kings XI Punjab',
       'bat_team_Kolkata Knight Riders', 'bat_team_Mumbai Indians',
       'bat_team_Rajasthan Royals', 'bat_team_Royal Challengers Bangalore',
       'bat_team_Sunrisers Hyderabad', 'bowl_team_Chennai Super Kings',
       'bowl_team_Delhi Daredevils', 'bowl_team_Kings XI Punjab',
       'bowl_team_Kolkata Knight Riders', 'bowl_team_Mumbai Indians',
       'bowl_team_Rajasthan Royals', 'bowl_team_Royal Challengers Bangalore',
       'bowl_team_Sunrisers Hyderabad']

def predict_score_raw(runs, wickets, overs, runs_last_5, wickets_last_5, striker, non_striker, bat_team, bowl_team):
    bat_team='bat_team_'+bat_team
    bat_team_index=cols.index(bat_team)
    
    bowl_team='bowl_team_'+bowl_team
    bowl_team_index=cols.index(bowl_team)
    
    X_temp=np.array([int(runs), int(wickets), float(overs), int(runs_last_5), int(wickets_last_5), int(striker), int(non_striker)])
    X_pred=np.zeros(23)
    X_pred[0:7]=X_temp
    X_pred[bowl_team_index]=1
    X_pred[bat_team_index]=1
    
    model = pickle.load(open('model.pkl', 'rb'))
    predicted_score=round(model.predict([X_pred])[0])
    predict_final=f'{int(predicted_score-10)}-{int(predicted_score+10)}'
    return predict_final


@csrf_exempt
@require_http_methods(["POST"])
def predict_score(request):
    keys = ['runs', 'wickets', 'overs', 'runs_last_5', 'wickets_last_5', 'striker', 'non-striker', 'bat_team', 'bowl_team']

    if all(key in request.POST for key in keys):
        values = [request.POST[key] for key in keys]
        predicted_score=predict_score_raw(*values)
        return JsonResponse({'status': 'success', 'data':{'predicted_score': predicted_score}})
    else:
        return JsonResponse({'status': 'failed'})