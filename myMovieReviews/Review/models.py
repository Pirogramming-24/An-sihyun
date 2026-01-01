from django.db import models

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=32)
    director = models.CharField(max_length=32)
    actor = models.CharField(max_length=32)
    release = models.PositiveIntegerField()
    
    GENRE_CHOICES=[
        ('default', '------'),
        ('action', '액션'),
        ('romance', '로맨스'),
        ('SF', 'SF'),
        ('comedy', '코미디'),
        ('documentary', '다큐멘터리')
    ]

    genre = models.CharField(max_length=32, choices=GENRE_CHOICES, default='default')
    star = models.DecimalField(max_digits=2, decimal_places=1)
    runningtime = models.PositiveIntegerField()
    review_content = models.TextField()


# 영화 제목, 감독, 주연, 장르, 별점, 러닝타임, 리뷰 내용. 