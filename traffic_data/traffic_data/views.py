from django.shortcuts import render
from django.views.generic import TemplateView
from database.models import Tweet

# Create your views here.


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        data = [
            Tweet.objects.filter(sentiment_string="pos").count(),
            Tweet.objects.filter(sentiment_string="neu").count(),
            Tweet.objects.filter(sentiment_string="neg").count()
        ]
        return render(request, 'index.html', {'dbdata': data})
