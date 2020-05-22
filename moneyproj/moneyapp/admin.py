from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Person, Budget


class BudgetInline(admin.TabularInline):
    model = Budget
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'user_profile', 'currency', 'auth_code', 'total_account', 'image', 'id')
    readonly_fields = ('get_image', 'id')
    inlines = [BudgetInline]
    save_on_top = True
    search_fields = ('name',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50", height="60" ')
    get_image.short_description = 'Image'


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('person', 'income_value', 'expense_value', 'category', 'added_date', 'id')
    list_filter = ('category', 'added_date', )
    search_fields = ('person', 'income_value', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'budget_choice', 'id')
    list_filter = ('title',)
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.site_title = "Money Control"
admin.site.site_header = "Money Control"
