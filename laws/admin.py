from django.contrib import admin
from .models import Law, LawVersion

admin.site.register(Law)
admin.site.register(LawVersion)

from .models import ActivityLog

admin.site.register(ActivityLog)