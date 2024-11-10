from fasttower.db import models

class FastTowerModel(models.Model):
    say = models.CharField(max_length = 100, default = "Hello World!")