from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^wordcloud/', views.WordCloudView.as_view(), name='word_cloud'),
    url(r'^linechart/', views.LineChartView.as_view(), name='line_chart'),
]
