from django.contrib import admin

from .models import (TechnicianDetails, Specialization, TechnicianSpecializations,
                     ShopFeedbackRating, SkillBadge)


class TechnicianDetailsConfig(admin.ModelAdmin):
    search_fields = ('autouser', 'skill_badge')
    list_display = ('rating', 'shop_goal', 'lat', 'lng', 'id')

    fieldsets = (
        (None, {'fields': ('autouser', 'profile_picture', 'rating', 'skill_badge')}),
        ('Location', {'fields': ('lat', 'lng')}),
        ('Description', {'fields': ('shop_description', 'shop_goal')})
    )

    add_fieldsets = (
        (None, {'fields': ('autouser', 'profile_picture', 'rating', 'skill_badge')}),
        ('Location', {'fields': ('lat', 'lng')}),
        ('Description', {'fields': ('shop_description', 'shop_goal')})
    )


class SpecializationConfig(admin.ModelAdmin):
    list_display = ('id', 'name',)

    fieldsets = (
        (None, {'fields': ('name',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('name',)}),
    )


class TechnicianSpecializationsConfig(admin.ModelAdmin):
    search_fields = ('technician', 'specialization',)
    # list_display = ('technician', 'specialization')

    fieldsets = (
        (None, {'fields': ('technician', 'specialization')}),
    )

    add_fieldsets = (
        (None, {'fields': ('specialization', 'technician')}),
    )


class ShopFeedbackRatingConfig(admin.ModelAdmin):
    search_fields = ('technician', 'autouser')
    list_display = ('id', 'rating', 'description')

    fieldsets = (
        (None, {'fields': ('description', 'rating')}),
        ('Stakeholders', {'fields': ('technician', 'autouser')})
    )

    add_fieldsets = (
        (None, {'fields': ('description', 'rating')}),
        ('Stakeholders', {'fields': ('technician', 'autouser')})
    )


class SkillBadgeConfig(admin.ModelAdmin):
    search_fields = ('badge',)
    list_display = ('id', 'badge')

    fieldsets = (
        (None, {'fields': ('badge',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('badge',)}),
    )


admin.site.register(TechnicianDetails, TechnicianDetailsConfig)
admin.site.register(Specialization, SpecializationConfig)
admin.site.register(TechnicianSpecializations, TechnicianSpecializationsConfig)
admin.site.register(ShopFeedbackRating, ShopFeedbackRatingConfig)
admin.site.register(SkillBadge, SkillBadgeConfig)

# local admin credentials are email - example@gmail.com, password - 0000
