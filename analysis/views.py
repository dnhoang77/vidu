from typing import Sequence
from django.shortcuts import render
import pandas as pd
import os
from django.conf import settings
# Create your views here.
def work_with_series(request):
    views2 = pd.read_csv(os.path.join(settings.MEDIA_ROOT,'analysis/data_views.csv'), squeeze=True)
    views2 = pd.DataFrame({'Views':views2})
    headviews2 = views2.head().to_html()
    return render(request,'analysis/series.html',{'headviews2':headviews2})