from django.db import models
from django.utils.translation import gettext_lazy as _ #translation tools for implementing translation throughout the whole application.

# Create your models here.
#We’re gonna create the table below to save the different types of delivery options I’m going to offer in my system. 
# So we want to store for example delivery choices as a list of options here. There might be three main (different types of) delivery choices that the user can choose from.
class DeliveryOptions(models.Model):
    """
    The Delivery methods table contining all delivery
    """

    DELIVERY_CHOICES = [  #This is a class-level constant that defines the available delivery methods as a list of tuples of (value, display name). 
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery"),
    ]

    delivery_name = models.CharField(
        verbose_name=_("delivery_name"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_price = models.DecimalField(
        verbose_name=_("delivery price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES, #The option that the user selected from the available options in the 'DELIVERY_CHOICES' list above.
        verbose_name=_("delivery_method"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_timeframe = models.CharField( #we're gonna set a manual time frame (one to two days).
        verbose_name=_("delivery timeframe"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_window = models.CharField( #This is just gonna refer to the time of day that your package might be delivered
        verbose_name=_("delivery window"),
        help_text=_("Required"),
        max_length=255,
    )
    order = models.IntegerField(verbose_name=_("list order"), help_text=_("Required"), default=0) #An 'IntegerField' that determines the order in which delivery options appear in lists or dropdowns. It defaults to 0.
    is_active = models.BooleanField(default=True) #we can make the delivery option active or inactive, based upon whether we want to provide that service.

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self):
        return self.delivery_name


# class PaymentSelections(models.Model):#This model stores different types of payment selections available for customers during checkout. we can hook this up to the payment page And I can then output the different payment selections that are available and I can then make them active or inactive.
#     """
#     Store payment options
#     """

#     name = models.CharField(
#         verbose_name=_("name"),
#         help_text=_("Required"),
#         max_length=255,
#     )

#     is_active = models.BooleanField(default=True)

#     class Meta:
#         verbose_name = _("Payment Selection")
#         verbose_name_plural = _("Payment Selections")

#     def __str__(self):
#         return self.name