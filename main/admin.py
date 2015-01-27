from main.models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from mce_filebrowser.admin import MCEFilebrowserAdmin
from tinymce.widgets import TinyMCE
from django.core.urlresolvers import reverse
from sorl.thumbnail.admin import AdminImageMixin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin



# Register your models here.

class CommentInlineAdmin(admin.TabularInline):
    fieldsets = (
        (
            None,
            {
                'fields': ('title', 'content')
            }
        ),
    )

    model = Comment
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    ordering = ('-id',)
    prepopulated_fields = {'slug': ('title',)}


class PostResource(resources.ModelResource):
    class Meta:
        model = Post
        fields = ('title', 'content', 'category')
        widgets = {'date': {'format': '%d.%m.%Y'}, }


class PostAdmin(AdminImageMixin, ImportExportActionModelAdmin, MCEFilebrowserAdmin):
    resource_class = PostResource
    inlines = (CommentInlineAdmin,)
    list_display = ('title', 'category', 'date', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('date', 'category')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('content1', 'content2'):
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ))
        return super(PostAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'post', 'date')
    ordering = ('-id',)
    list_filter = ('date',)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    ordering = ('id',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def post_tag(self):
        return "\n".join([p.post for p in self.post.all()])


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'name', 'gender', 'avatar', 'email', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'name', 'gender', 'avatar', 'email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the
        return self.initial["password"]


class MyUserAdmin(AdminImageMixin, UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'name', 'gender', 'preview_avatar', 'email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'gender', 'avatar', 'date_of_birth', 'email')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'gender', 'avatar', 'email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)