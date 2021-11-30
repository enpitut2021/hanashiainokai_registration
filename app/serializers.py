from rest_framework import serializers

from .models import App

class MeiboSerializer(serializers.ModelSerializer):
  class Meta:
    model = App
    fields = ('summary', 'start_time', 'end_time','data','created_at')


    # summary = models.CharField('概要', max_length=50)
    # description = models.TextField('詳細な説明', blank=True)
    # start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    # end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))
    # date = models.DateField('日付')
    # created_at = models.DateTimeField('作成日', default=timezone.now)