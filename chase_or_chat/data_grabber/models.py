from django.db import models


class laptop(models.Model):
    url = models.CharField(max_length=120)
    title = models.CharField(max_length=100)
    cpu = models.CharField(max_length=50)
    ram = models.CharField(max_length=30)
    ram_num = models.IntegerField()
    hardware = models.CharField(max_length=40)
    screen = models.CharField(max_length=40)
    screen_num = models.FloatField()
    price = models.IntegerField()
    else_spec = models.CharField(max_length=300)
    picture = models.CharField(max_length=300)


class laptopManager(models.Manager):

    '''
    currently, use manage to solve the filter problem...

    sort for string data needed to extract the integer field
    '''

    def myfilter(self, **kwarg):
        '''
        according to the keyword you give,
        '''
        pass
