from django.db import models

# Create your models here.

class DevTool(models.Model):
    name = models.CharField(max_length=32)
    kind = models.CharField(max_length=32)
    content = models.TextField()
    def __str__(self):
        return self.name


class Idea(models.Model):
    title = models.CharField(max_length=32)
    image = models.ImageField()
    content = models.TextField()
    interest = models.IntegerField()
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE, related_name='ideas')
    def __str__(self):
        return self.title
    

class IdeaStar(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='star')



