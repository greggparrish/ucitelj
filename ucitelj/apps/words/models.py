from django.db import models


class WordRole(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class Rijec(models.Model):
    term = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.term

    class Meta:
        verbose_name_plural = "Riječi"


class Word(models.Model):
    term = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.term


class Definition(models.Model):
    GENDER_CHOICES = (
        (0, 'M'),
        (1, 'F'),
        (2, 'N'),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    word = models.ForeignKey(Word, max_length=100, on_delete=models.CASCADE)
    rijec = models.ForeignKey(Rijec, max_length=100, on_delete=models.CASCADE)
    plural = models.BooleanField(default=False)
    wordrole = models.ForeignKey(WordRole, on_delete=models.PROTECT)
    def __str__(self):
        return "%s :  %s" % (self.rijec, self.word)
