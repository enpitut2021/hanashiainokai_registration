from django.db import models
import datetime
from django.utils import timezone
import uuid

class Schedule(models.Model):
    """スケジュール"""
#    Schedule_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False) #独立のidを作る
    summary = models.CharField('概要', max_length=50)
    description = models.TextField('詳細な説明', blank=True)
    start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))
    room = models.CharField('勉強部屋', max_length=1)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.summary
