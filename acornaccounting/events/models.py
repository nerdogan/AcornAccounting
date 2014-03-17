from caching.base import CachingManager, CachingMixin
from localflavor.us.models import USStateField
from django.core.urlresolvers import reverse
from django.db import models


class Event(CachingMixin, models.Model):
    """Hold information about Events."""
    name = models.CharField(max_length=150)
    number = models.PositiveIntegerField()
    date = models.DateField()
    city = models.CharField(max_length=50)
    # TODO: Deprecated in either Django 1.6 or 1.7
    state = USStateField()

    objects = CachingManager()

    class Meta:
        """Order Events by Date."""
        ordering = ['date']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Return the URL of the Event's Details Page."""
        return reverse('events.views.show_event_detail',
                       kwargs={'event_id': self.id})

    def get_net_change(self):
        """Return the sum of all related credit and debit charges.

        :rtype: :class:`~decimal.Decimal`

        """
        _, _, net_change = self.transaction_set.get_totals(net_change=True)
        return net_change
