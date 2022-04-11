from django.db import models


class ProductFamily(models.Model):
    TRANSMISSION = "Transmission"
    MOBILE = "Mobile"
    ACCESS = "Access"
    POWER = "Power"
    IP = "IP"
    CHOICES = [(x, x) for x in (ACCESS, IP, MOBILE, POWER, TRANSMISSION)]

    name = models.CharField(max_length=100,)
    description = models.TextField(
        null=True,
        blank=True,
    )
    domain = models.CharField(
        max_length=max([len(y) for (x, y) in CHOICES]),
        choices=CHOICES,
    )

    def __str__(self):
        return f"{self.domain} {self.name}"

    class Meta:
        verbose_name_plural = 'Product families'


class Product(models.Model):
    PRE_ALPHA = "PRE ALPHA"
    ALPHA = "ALPHA"
    BETA = "BETA"
    RELEASE_CANDIDATE = "RELEASE CANDIDATE"
    STABLE_RELEASE = "STABLE RELEASE"
    END_OF_SUPPORT = "END OF SUPPORT"

    CHOICES = [(x, x) for x in (PRE_ALPHA, ALPHA, BETA, RELEASE_CANDIDATE, STABLE_RELEASE, END_OF_SUPPORT)]

    name = models.CharField(max_length=100,)
    family = models.ForeignKey(
        ProductFamily,
        on_delete=models.RESTRICT,
    )
    features = models.TextField(
        null=True,
        blank=True,
    )
    version = models.CharField(max_length=30,)
    stability = models.CharField(
        max_length=max([len(y) for (x, y) in CHOICES]),
        choices=CHOICES,
    )
    date_of_release = models.DateField(
        null=True,
        blank=True,
    )
    end_of_support = models.DateField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f"Domain: {self.family.domain} Product: {self.name} Version: {self.version}"
