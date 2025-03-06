from django.db import models

# Create your models here.
class House(models.Model):
    house_id = models.CharField(max_length=50, unique=True)  # 房屋 ID，確保唯一
    created_at = models.DateTimeField(auto_now_add=True)  # 新增時間

    def __str__(self):
        return self.house_id