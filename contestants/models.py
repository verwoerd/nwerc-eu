from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    ICPC_name = models.CharField(_('ICPC name'), max_length=3)
    name = models.CharField(_('name'), max_length=55, blank=True, null=True)
    iso_3166_1 = models.CharField(_('ISO 3166-1 Alpha 2 code'), max_length=2, blank=True, null=True)

    def get_flag_url(self):
        return 'img/flags/%s.png' % self.iso_3166_1

    def __unicode__(self):
        if self.name:
            return self.name
        return self.ICPC_name

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class Institution(models.Model):
    institution_id = models.IntegerField(_('institution_id'), primary_key=True)
    name = models.CharField(_('name'), max_length=255, blank=True, null=True)
    short_name = models.CharField(_('short name'), max_length=55, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    logo = models.ImageField(_('logo'), upload_to='institutions', blank=True, null=True)

    def __unicode__(self):
        return self.name


class Person(models.Model):
    person_id = models.IntegerField(_('person id'), primary_key=True)
    title = models.CharField(_('title'), max_length=20, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True, null=True)
    prefered_name = models.CharField(_('prefered name'), max_length=120, blank=True, null=True)
    certificate_name = models.CharField(_('certificate name'), max_length=120, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    date_of_birth = models.DateField(_('Date of birth'), blank=True, null=True)
    gender = models.CharField(_('gender'), max_length=1, choices=(('M', 'MALE'), ('F', 'FEMALE'), ), blank=True,
                              null=True)
    shirt_size = models.CharField(_('shirt size'), max_length=10, blank=True, null=True)

    @property
    def is_coach(self):
        try:
            TeamPerson.objects.get(person=self, role='COACH')
            return True
        except TeamPerson.DoesNotExist:
            return False

    def __unicode__(self):
        return self.prefered_name


class Team(models.Model):
    class Meta:
        ordering = ('name', )

    team_id = models.IntegerField(_('team id'), primary_key=True)
    name = models.CharField(_('name'), max_length=255, blank=True, null=True)
    institution = models.ForeignKey(Institution, blank=True, null=True)
    status = models.CharField(_('status'), max_length=10, blank=True, null=True)
    created = models.DateField(_('created'), blank=True, null=True)

    members = models.ManyToManyField(Person, through='TeamPerson', related_name='teams', blank=True, null=True)

    def __unicode__(self):
        return self.name


class TeamPerson(models.Model):
    ROLE_CHOICES = (
        ('CONTESTANT', _('Contestant')),
        ('COACH', _('Coach')),
        ('RESERVE', _('Reserve')),
        ('ATTENDEE', _('Attendee')),
    )

    person = models.ForeignKey('Person')
    team = models.ForeignKey('Team')
    role = models.CharField(_('role'), max_length=15, choices=ROLE_CHOICES)