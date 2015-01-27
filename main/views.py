from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from main.models import *
from main.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.paginator import FlynsarmyPaginator, FlynsarmyPage
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.utils.http import urlsafe_base64_decode
from django.conf import settings





# Create your views here.
def mainpage(request):
    posts = Post.objects.all().order_by('-date')
    categories = Category.objects.all().order_by('-id')
    paginator = FlynsarmyPaginator(posts, 2, adjacent_pages=2) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render_to_response('index.html', {'posts': posts, 'categories': categories}, context_instance=RequestContext(request))

def categorypage(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    paginator = FlynsarmyPaginator(posts, 2, adjacent_pages=2) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render_to_response('category.html', {'posts': posts, 'category': category}, context_instance=RequestContext(request))

def postpage(request, category_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    if request.method == 'POST' and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            request.session.set_expiry(10)
            request.session['pause'] = True
            return HttpResponseRedirect(reverse("view_post", kwargs={'category_slug': category_slug, 'post_slug': post_slug}))
        else:
            return render_to_response('post.html', {'post': post, 'form': form}, context_instance=RequestContext(request))

    form = CommentForm()
    return render_to_response('post.html', {'post': post, 'form': form}, context_instance=RequestContext(request))

def tagpage(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag)
    return render_to_response('tag.html', {'posts': posts, 'tag': tag}, context_instance=RequestContext(
        request))


def PosterRegistration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = MyUser.objects.create_user(username=form.cleaned_data['username'],name=form.cleaned_data['name'], email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'], gender=form.cleaned_data['gender'], date_of_birth=form.cleaned_data['date_of_birth'])
            user.save()
            return HttpResponseRedirect('/')
        else:
            return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = RegistrationForm()
        return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))


@login_required()
def Profile(request):
    return render_to_response('profile.html', context_instance=RequestContext(request))


def LoginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        next = request.REQUEST['next']
        formlogin = LoginForm(request.POST)
        if formlogin.is_valid():
            username = formlogin.cleaned_data['username']
            password = formlogin.cleaned_data['password']
            poster = authenticate(username=username, password=password)
            if poster is not None:
                login(request, poster)
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect('/')
            else:
                return render_to_response('login.html', {'form': formlogin}, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', {'form': formlogin}, context_instance=RequestContext(request))
    else:
        formlogin = LoginForm()
        return render_to_response('login.html', {'form': formlogin}, context_instance=RequestContext(request))


def LogoutRequest(request):
    next = request.REQUEST['next']
    logout(request)
    if next:
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect('/')




# @csrf_protect
# def password_reset(request, is_admin_site=False,
#                    template_name='registration/password_reset_form.html',
#                    email_template_name='registration/password_reset_email.html',
#                    subject_template_name='registration/password_reset_subject.txt',
#                    password_reset_form=PasswordResetForm,
#                    token_generator=default_token_generator,
#                    post_reset_redirect=None,
#                    from_email=None,
#                    current_app=None,
#                    extra_context=None,
#                    html_email_template_name=None):
#     if post_reset_redirect is None:
#         post_reset_redirect = reverse('password_reset_done')
#     else:
#         post_reset_redirect = resolve_url(post_reset_redirect)
#     if request.method == "POST":
#         form = password_reset_form(request.POST)
#         if form.is_valid():
#             opts = {
#                 'use_https': request.is_secure(),
#                 'token_generator': token_generator,
#                 'from_email': from_email,
#                 'email_template_name': email_template_name,
#                 'subject_template_name': subject_template_name,
#                 'request': request,
#                 'html_email_template_name': html_email_template_name,
#             }
#             if is_admin_site:
#                 opts = dict(opts, domain_override=request.get_host())
#             form.save(**opts)
#             return HttpResponseRedirect(post_reset_redirect)
#     else:
#         form = password_reset_form()
#     context = {
#         'form': form,
#         'title': ('Password reset'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#     return TemplateResponse(request, template_name, context,
#                             current_app=current_app)
#
#
# def password_reset_done(request,
#                         template_name='registration/password_reset_done.html',
#                         current_app=None, extra_context=None):
#     context = {
#         'title': ('Password reset successful'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#     return TemplateResponse(request, template_name, context,
#                             current_app=current_app)
#
#
# # Doesn't need csrf_protect since no-one can guess the URL
# @sensitive_post_parameters()
# @never_cache
# def password_reset_confirm(request, uidb64=None, token=None,
#                            template_name='registration/password_reset_confirm.html',
#                            token_generator=default_token_generator,
#                            set_password_form=SetPasswordForm,
#                            post_reset_redirect=None,
#                            current_app=None, extra_context=None):
#     """
#     View that checks the hash in a password reset link and presents a
#     form for entering a new password.
#     """
#     UserModel = get_user_model()
#     assert uidb64 is not None and token is not None  # checked by URLconf
#     if post_reset_redirect is None:
#         post_reset_redirect = reverse('password_reset_complete')
#     else:
#         post_reset_redirect = resolve_url(post_reset_redirect)
#     try:
#         uid = urlsafe_base64_decode(uidb64)
#         user = UserModel._default_manager.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#         user = None
#
#     if user is not None and token_generator.check_token(user, token):
#         validlink = True
#         title = ('Enter new password')
#         if request.method == 'POST':
#             form = set_password_form(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(post_reset_redirect)
#         else:
#             form = set_password_form(user)
#     else:
#         validlink = False
#         form = None
#         title = ('Password reset unsuccessful')
#     context = {
#         'form': form,
#         'title': title,
#         'validlink': validlink,
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#     return TemplateResponse(request, template_name, context,
#                             current_app=current_app)
#
# def password_reset_complete(request,
#                             template_name='registration/password_reset_complete.html',
#                             current_app=None, extra_context=None):
#     context = {
#         'login_url': resolve_url(settings.LOGIN_URL),
#         'title': ('Password reset complete'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#     return TemplateResponse(request, template_name, context,
#                             current_app=current_app)

