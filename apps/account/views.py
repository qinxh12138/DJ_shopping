import uuid

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.template import loader



# Create your views here.
from DJ_shopping import settings
from apps.main.models import User


def login_test(request):
    if request.method == 'GET':
        next = request.GET.get('next')
        return render(request, 'login.html', {'msg': "请输入正确的格式"}, {'next', next})
    elif request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            return_url = request.POST.get('next')
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user:
                    if user.is_active:
                        if return_url:
                            login(request, user)
                            return redirect(return_url)
                        else:
                            login(request, user)
                            return redirect('/')
                    else:
                        return render(request, 'login.html', {'msg': "账号已被禁用,请与管理员联系!"})
                else:
                    return render(request, 'login.html', {'msg': "用户不存在或账号密码错误"})
            else:
                return render(request, 'login.html', {'msg': "请输入正确格式"})
        except:
            return render(request, 'login.html', {'msg': "参数错误"})
    else:
        return render(request, 'login.html', {'msg': "请求错误"})


def register_test(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'msg': "请输入正确的格式"})
    elif request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            if username and password:
                user = User.objects.filter(username=username)
                if user:
                    return render(request, 'login.html', {'msg': "该用户已经存在,请直接登录"})
                else:
                    # 保存用户的操作
                    user = User.objects.create_user(username=username, password=password, phone=phone, email=email,
                                                    is_active=0)
                    if user:
                        # 如果注册成功  直接记住用户登录状态,跳转首页
                        #               跳转登录界面,让用户重新登录一次
                        # 记住用户状态
                        # 底层做了两个操作,
                        # 第一个操作将用户信息保存到session中
                        # 第二个操作将用户信息绑定到request对象
                        # request.user
                        tooken = uuid.uuid4()
                        cache.set(tooken, user.id)
                        active_url = f'http://127.0.0.1:8000/account/active/?uid={tooken}'
                        content = loader.render_to_string('mail.html',
                                                          request=request,
                                                          context={'username': username, 'active_url': active_url})
                        send_active_mail(subject='91电影网激活邮件', content=content, to=[email])
                        return redirect('/')
                    # 用户注册成功
            else:
                return render(request, 'register.html', {'msg': "请输入正确格式"})
        except:
            return render(request, 'register.html', {'msg': "请求错误"})


@login_required()
def logout_test(request):
    logout(request)
    return redirect('/')


def active_account(request):
    tooken = request.GET.get('uid')
    uid = cache.get(tooken)
    if uid:
        try:
            User.objects.filter(id=uid).update(is_active=1)
            return redirect('/')
        except:
            return render(request, 'register.html', {'msg': "请求错误"})
    else:
        return render(request, 'register.html', {'msg': "激活失败"})


def hello_mail(request):
    """
        subject,标题
        message, 邮件的内容
        from_email,发送邮件者
        recipient_list,  接受邮件列表
        html_message = 邮件的内容,以html格式显示邮件内容
    :param request:
    :return:
    """
    # send_mail(subject='xxx线上xxx注册邮件',
    #           message='注册成功可以观看更多高清无码的xxx',
    #           from_email=settings.EMAIL_HOST_USER,
    #           recipient_list=['18614068889@163.com']
    #           )
    content = loader.render_to_string('mail.html', request=request)
    send_mail(subject='澳门皇家赌场线上美女荷官在线注册邮件',
              message='',
              html_message=content,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=['18327863113@163.com']
              )

    return render(request, 'msg.html')


def send_active_mail(subject='', content=None, to=None):
    send_mail(subject=subject,
              message='',
              html_message=content,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=to
              )
