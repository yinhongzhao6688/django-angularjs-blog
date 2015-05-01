# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from app.utils import *
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from app.myblog.models import *
from misaka import Markdown, HtmlRenderer
import math
import markdown
import gfm
# Create your views here.


@ensure_csrf_cookie
def index(req):
    req.session.set_expiry(5)
    return render_to_response('index.html')


def code(req):
    return render_to_response('code.html')


def lab(req):
    return render_to_response('lab.html')

def blog(req, bid=None):
    if bid is not None:
        if bid == '#':
            return render_to_response('blog_detail.html')
        blog = get_object_or_404(Article, id=bid)
        return render_to_response('blog_detail.html')
    return render_to_response('blog.html')


def classify(req, bid=None):
    return render_to_response("blog.html")


def tag(req, bid=None):
    return render_to_response("blog.html")


def about(req):
    return render_to_response('about.html')


def know(req):
    return render_to_response('knowledge.html')


def get_classify(req, cid=None):
    body={}
    print cid
    blog_list = Article.objects.filter(publish=True, classification__id=cid).order_by('-create_time')
    total = blog_list.count()
    total_page = math.ceil(float(total) / 4.0)
    paginator = Paginator(blog_list, 4)
    page_num = 1
    try:
        page_num = int(req.GET.get('page'))
        print page_num
        blog_list = paginator.page(page_num)
    except PageNotAnInteger:
        blog_list = paginator.page(1)
    except EmptyPage:
        blog_list = []
    except:
        blog_list = paginator.page(page_num)
    blog_json = model_serializer(blog_list, serializer='dict', datetime_format='string')
    for i, itm in enumerate(blog_list):
        # blog_json[i]['content'] = gfm.markdown(gfm.gfm(itm.content[:400]))
        blog_json[i]['content'] = markdown.markdown(itm.content[:400], ['codehilite'])
        blog_json[i]['classify'] = model_serializer(itm.classification, include_attr=['c_name', 'id'])
        blog_json[i]['tags'] = model_serializer(itm.tags.all(), include_attr=['tag_name', 'id'])
    page_list = []
    for i in range(1, int(total_page) + 1):
        paged={}
        paged['page'] = i
        if i == page_num:
            paged['active'] = True
        else:
            paged['active'] = False
        page_list.append(copy.copy(paged))
    if page_num == total_page:
        nextp = 0
        prep = total_page - 1
    elif page_num == 1:
        prep = 0
        nextp = page_num + 1
    else:
        prep = page_num - 1
        nextp = page_num + 1
    pagination = {'page': page_num,
                  'total_page': total_page,
                  'total': total,
                  'pre': prep,
                  'next': nextp,
                  'page_list': page_list}
    body['blog_list'] = blog_json
    body['pagination'] = pagination
    return HttpResponse(encodejson(1, body), content_type="application/json")


def get_tag(req, tid=None):
    body={}
    blog_list = Article.objects.filter(publish=True, tags__id=tid).order_by('-create_time')
    total = blog_list.count()
    total_page = math.ceil(float(total) / 4.0)
    paginator = Paginator(blog_list, 4)
    page_num = 1
    try:
        page_num = int(req.GET.get('page'))
        print page_num
        blog_list = paginator.page(page_num)
    except PageNotAnInteger:
        blog_list = paginator.page(1)
    except EmptyPage:
        blog_list = []
    except:
        blog_list = paginator.page(page_num)
    blog_json = model_serializer(blog_list, serializer='dict', datetime_format='string')
    for i, itm in enumerate(blog_list):
        # blog_json[i]['content'] = gfm.markdown(gfm.gfm(itm.content[:400]))
        blog_json[i]['content'] = markdown.markdown(itm.content[:400], ['codehilite'])
        blog_json[i]['classify'] = model_serializer(itm.classification, include_attr=['c_name', 'id'])
        blog_json[i]['tags'] = model_serializer(itm.tags.all(), include_attr=['tag_name', 'id'])
    page_list = []
    for i in range(1, int(total_page) + 1):
        paged={}
        paged['page'] = i
        if i == page_num:
            paged['active'] = True
        else:
            paged['active'] = False
        page_list.append(copy.copy(paged))
    if page_num == total_page:
        nextp = 0
        prep = total_page - 1
    elif page_num == 1:
        prep = 0
        nextp = page_num + 1
    else:
        prep = page_num - 1
        nextp = page_num + 1
    pagination = {'page': page_num,
                  'total_page': total_page,
                  'total': total,
                  'pre': prep,
                  'next': nextp,
                  'page_list': page_list}
    body['blog_list'] = blog_json
    body['pagination'] = pagination
    return HttpResponse(encodejson(1, body), content_type="application/json")


def searche_know(req, text):
    body={}

    total = know_list.count()
    total_page = math.ceil(float(total) / 2.0)
    paginator = Paginator(know_list, 2)
    page_num = 1
    try:
        page_num = int(req.GET.get('page'))
        print page_num
        know_list = paginator.page(page_num)
    except PageNotAnInteger:
        know_list = paginator.page(1)
    except EmptyPage:
        know_list = []
    except:
        know_list = paginator.page(page_num)
    know_json = model_serializer(know_list, datetime_format="string", deep=True)
    for i, itm in enumerate(know_list):
        if i == 0:
            know_json[i]['first'] = True
        else:
            know_json[i]['first'] = False
        know_json[i]['env'] = model_serializer(itm.env.all(), include_attr=['content'])
    page_list = []
    for i in range(1, int(total_page) + 1):
        paged={}
        paged['page'] = i
        if i == page_num:
            paged['active'] = True
        else:
            paged['active'] = False
        page_list.append(copy.copy(paged))
    if page_num == total_page:
        nextp = 0
        prep = total_page - 1
    elif page_num == 1:
        prep = 0
        nextp = page_num + 1
    else:
        prep = page_num - 1
        nextp = page_num + 1
    pagination = {'page': page_num,
                  'total_page': total_page,
                  'total': total,
                  'pre': prep,
                  'next': nextp,
                  'page_list': page_list}
    body['know_list'] = know_json
    body['pagination'] = pagination
    return HttpResponse(encodejson(1, body), content_type='application/json')


def get_know(req, text=None):
    body={}
    if text is not None:
        q_list = Knowledge.objects.filter(question__icontains=text, publish=True)
        a_list = Knowledge.objects.filter(answer__icontains=text, publish=True)
        know_list = q_list | a_list
        know_list = know_list.distinct().order_by('-create_time')
    else:
        know_list = Knowledge.objects.filter(publish=True).order_by('-create_time')
    total = know_list.count()
    total_page = math.ceil(float(total) / 2.0)
    paginator = Paginator(know_list, 2)
    page_num = 1
    try:
        page_num = int(req.GET.get('page'))
        print page_num
        know_list = paginator.page(page_num)
    except PageNotAnInteger:
        know_list = paginator.page(1)
    except EmptyPage:
        know_list = []
    except:
        know_list = paginator.page(page_num)
    know_json = model_serializer(know_list, datetime_format="string", deep=True)
    for i, itm in enumerate(know_list):
        if i == 0:
            know_json[i]['first'] = True
        else:
            know_json[i]['first'] = False
        know_json[i]['answer'] = markdown.markdown(itm.answer, ['codehilite'])
        # know_json[i]['answer'] = gfm.markdown(gfm.gfm(itm.answer))
        know_json[i]['env'] = model_serializer(itm.env.all(), include_attr=['content'])
    page_list = []
    for i in range(1, int(total_page) + 1):
        paged={}
        paged['page'] = i
        if i == page_num:
            paged['active'] = True
        else:
            paged['active'] = False
        page_list.append(copy.copy(paged))
    if page_num == total_page:
        nextp = 0
        prep = total_page - 1
    elif page_num == 1:
        prep = 0
        nextp = page_num + 1
    else:
        prep = page_num - 1
        nextp = page_num + 1
    pagination = {'page': page_num,
                  'total_page': total_page,
                  'total': total,
                  'pre': prep,
                  'next': nextp,
                  'page_list': page_list}
    body['know_list'] = know_json
    body['pagination'] = pagination
    return HttpResponse(encodejson(1, body), content_type='application/json')



def detail(req, bid):
    body={}
    blog_list = Article.objects.filter(id=bid, publish=True)
    all_blog = Article.objects.all().order_by('create_time')
    if not blog_list.exists():
        body['blog'] = ''
        return HttpResponse(encodejson(7, body), content_type='application/json')
    blog = blog_list[0]
    blog.read_count += 1
    blog.save()
    preb = '#'
    nextb = '#'
    pre_title = ''
    next_title = ''
    # print len(all_blog)
    for i, itm in enumerate(all_blog):
        if itm == blog:
            if i == 0:
                preb = itm.id
                pre_title = ''
            else:
                preb = all_blog[i-1].id
                pre_title = all_blog[i-1].caption
            if (i+1) == all_blog.count():
                nextb = itm.id
                next_title = ''
            else:
                nextb = all_blog[i+1].id
                next_title = all_blog[i+1].caption
            break

    pagination = {'pre_id': preb,
                  'next_id': nextb,
                  'pre_title': pre_title,
                  'next_title': next_title}
    comment_list_json = []
    comment_list = Comment.objects.filter(belong=blog).order_by("-create_time")
    have_comment = False
    if comment_list.exists():
        have_comment = True
        for itm in comment_list:
            comment_json = model_serializer(itm, datetime_format="string")
            comment_json['have_reply'] = False
            if itm.reply is True:
                comment_reply = itm.replys.all()
                reply_json = model_serializer(comment_reply, datetime_format="string")
                comment_json['have_reply'] = True
                comment_json['reply'] = reply_json
            comment_list_json.append(copy.copy(comment_json))
    blog.content = markdown.markdown(blog.content, ['codehilite'])
    # blog.content = gfm.markdown(gfm.gfm(blog.content))
    # rndr = HtmlRenderer()
    # md = Markdown(rndr)
    # blog.content = md.render(blog.content)
    blog_json = model_serializer(blog, deep=True, datetime_format="string")
    blog_json['tags'] = model_serializer(blog.tags.all())
    verify, code = create_verify_code()
    req.session['verify'] = code.upper()
    body['verify'] = verify
    body['blog'] = blog_json
    body['comment'] = comment_list_json
    body['have_comment'] = have_comment
    body['pagination'] = pagination
    return HttpResponse(encodejson(1, body), content_type='application/json')


def get_blog(req):
    body={}
    blog_list = Article.objects.filter(publish=True).order_by('-create_time')
    total = blog_list.count()
    total_page = math.ceil(float(total) / 4.0)
    paginator = Paginator(blog_list, 4)
    page_num = 1
    try:
        page_num = int(req.GET.get('page'))
        print page_num
        blog_list = paginator.page(page_num)
    except PageNotAnInteger:
        blog_list = paginator.page(1)
    except EmptyPage:
        blog_list = []
    except:
        blog_list = paginator.page(page_num)
    blog_json = model_serializer(blog_list, serializer='dict', datetime_format='string')
    for i, itm in enumerate(blog_list):
        # blog_json[i]['content'] = gfm.markdown(gfm.gfm(itm.content[:400]))
        blog_json[i]['content'] = markdown.markdown(itm.content[:400], ['codehilite'])
        blog_json[i]['classify'] = model_serializer(itm.classification, include_attr=['c_name', 'id'])
        blog_json[i]['tags'] = model_serializer(itm.tags.all(), include_attr=['tag_name', 'id'])
    page_list = []
    for i in range(1, int(total_page) + 1):
        paged={}
        paged['page'] = i
        if i == page_num:
            paged['active'] = True
        else:
            paged['active'] = False
        page_list.append(copy.copy(paged))
    if page_num == total_page:
        nextp = 0
        prep = total_page - 1
    elif page_num == 1:
        prep = 0
        nextp = page_num + 1
    else:
        prep = page_num - 1
        nextp = page_num + 1
    pagination = {'page': page_num,
                  'total_page': total_page,
                  'total': total,
                  'pre': prep,
                  'next': nextp,
                  'page_list': page_list}
    body['blog_list'] = blog_json
    body['pagination'] = pagination
    return HttpResponse(encodejson(1, body), content_type="application/json")


def get_tools(req):
    body={}
    latest_list = Article.objects.filter(publish=True).order_by('-create_time')
    if latest_list.count() > 5:
        latest_list = latest_list[0:5]
    classify_list = Classification.objects.all().order_by('-create_time')
    read_list = Article.objects.filter(publish=True).order_by('-read_count')
    if read_list.count() > 5:
        read_list = read_list[0:4]
    latest_json = model_serializer(latest_list, include_attr=['caption', 'create_time', 'id'], datetime_format="string")
    classify_json = model_serializer(classify_list, include_attr=['c_name', 'id'])
    read_json = model_serializer(read_list, include_attr=['caption', 'read_count', 'id'])
    body['latest_list'] = latest_json
    body['classify_list'] = classify_json
    body['read_list'] = read_json
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def submit_comment(req, bid=None):
    body={}
    if bid is None:
        body['fail_mes'] = 'id 不合法'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    verify = str(req.POST.get('verify')).upper()
    if verify != req.session.get('verify'):
        body['fail_mes'] = '验证码错误'
        return HttpResponse(encodejson(12, body), content_type='application/json')
    content = req.POST.get('content')
    nick = req.POST.get('nick')
    blog_list = Article.objects.filter(id=bid)
    if not blog_list.exists():
        body['fail_mes'] = 'id 不合法'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    blog = blog_list[0]
    blog.comment_count += 1
    blog.save()
    if nick == '' or nick is None:
        nick = '匿名用户'
    new_comment = Comment(content=content, author=nick, belong=blog)
    new_comment.save()
    # print new_comment.content
    return HttpResponse(encodejson(1, body), content_type='application/json')


def refresh_verify(req):
    body={}
    verify, code = create_verify_code()
    req.session['verify'] = code.upper()
    body['verify'] = verify
    return HttpResponse(encodejson(1, body), content_type="application/json")


def get_index(req):
    body={}
    blog_list = Article.objects.filter(publish=True).order_by('-create_time')
    all_blog = Article.objects.all().order_by('create_time')
    if not blog_list.exists():
        body['blog'] = ''
        return HttpResponse(encodejson(7, body), content_type='application/json')
    blog = blog_list[0]
    blog.read_count += 1
    blog.save()
    preb = '0'
    nextb = '0'
    pre_title = ''
    next_title = ''
    # print len(all_blog)
    for i, itm in enumerate(all_blog):
        if itm == blog:
            if i == 0:
                preb = itm.id
                pre_title = ''
            else:
                preb = all_blog[i-1].id
                pre_title = all_blog[i-1].caption
            if (i+1) == all_blog.count():
                nextb = itm.id
                next_title = ''
            else:
                nextb = all_blog[i+1].id
                next_title = all_blog[i+1].caption
            break

    pagination = {'pre_id': preb,
                  'next_id': nextb,
                  'pre_title': pre_title,
                  'next_title': next_title}
    blog.content = markdown.markdown(blog.content)
    blog_json = model_serializer(blog, deep=True, datetime_format="string")
    blog_json['tags'] = model_serializer(blog.tags.all())
    body['blog'] = blog_json
    body['pagination'] = pagination
    return HttpResponse(encodejson(1, body), content_type='application/json')