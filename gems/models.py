from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=64, default='anonymous')
    spent_money = models.IntegerField()
    gems = models.TextField()

    def __str__(self):
        return f'{self.username} {self.spent_money} {self.gems} '


class Deal(models.Model):
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)
    spent_money = models.IntegerField()
    gem_name = models.CharField(max_length=64)
    gems = models.IntegerField()
    date = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.username} {self.spent_money} {self.gem_name.name} {self.gems} {self.date} '
