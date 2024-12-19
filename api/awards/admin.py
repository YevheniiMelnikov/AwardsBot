from django.contrib import admin
from .models import User, Nomination, Candidate

admin.site.register(User)
admin.site.register(Nomination)
admin.site.register(Candidate)
