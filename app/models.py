from django.db import models
import datetime
from django.utils import timezone
import uuid
from django.core.validators import RegexValidator

class Discord_User(models.Model):
    discord_regex = RegexValidator(regex=r'^.{3,32}#[0-9]{4}$', message='name#0000の形式で入力してください')
    discord_name = models.CharField('Discordユーザ名', default="", max_length=37, validators=[discord_regex])
    
    def __str__(self):
        return self.discord_name

class Schedule(models.Model):
    """スケジュール"""
#    Schedule_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False) #独立のidを作る
    summary = models.CharField('概要', max_length=50)
    description = models.TextField('詳細な説明', blank=True)
    start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))
    room = models.CharField('勉強部屋', max_length=1)
    discord_regex = RegexValidator(regex=r'^.{3,32}#[0-9]{4}$', message='name#0000の形式で入力してください')
    creator = models.CharField('Discordユーザ名', default="", max_length=37, validators=[discord_regex])
    participants = models.ManyToManyField(Discord_User, blank=True)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.summary
