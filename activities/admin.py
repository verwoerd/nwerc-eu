from django.contrib import admin

from models import Activity, Subscription


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fields = ['person', ]
    extra = 0


class ActivityAdmin(admin.ModelAdmin):
    inlines = [SubscriptionInline, ]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['person', 'activity', 'mail_sent']
    list_filter = ['activity', ]


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Subscription, SubscriptionAdmin)