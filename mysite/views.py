from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
import pymysql
import time

def page_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        conn = pymysql.connect(host="localhost", user="root", password="root", database="user", charset="utf8")
        cursor = conn.cursor()
        dic = {
            'same': 'false',
            'not_same': 'false',
            'not_in': 'false',
            'wrong': 'false'
        }
        username = request.POST['username']
        password = request.POST['password']
        passwordagain = request.POST['passwordagain']
        sno = request.POST['sno']
        spassword = request.POST['spassword']
        email = request.POST['email']
        cursor.execute('select username from user where username=%s', username)
        uname = cursor.fetchone()
        if uname:
            dic['same'] = 'true'
        if password != passwordagain:
            dic['not_same'] = 'true'
        cursor.execute('select sno,spassword from school where sno=%s', sno)
        sn = cursor.fetchone()
        if not sn:
            dic['not_in'] = 'true'
        elif spassword != sn[1]:
            dic['wrong'] = 'true'
        if dic['same'] == 'true' or dic['not_same'] == 'true' or dic['not_in'] == 'true' or dic['wrong'] == 'true':
            return render(request, 'register.html', dic)
        else:
            cursor.execute('insert into user values(%s,%s,%s,%s)', [username, password, sno, email])
            conn.commit()
            conn.close()
            return HttpResponseRedirect('/successful')
def successful_register(request):
    HttpResponse("注册成功！等待跳转。。。")
    time.sleep(3)
    return HttpResponseRedirect('/login')



def page_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        conn = pymysql.connect(host="localhost", user="root", password="root", database="user", charset="utf8")
        cursor = conn.cursor()
        rp = {'r': 'true'}
        username = request.POST['username']
        password = request.POST['password']
        cursor.execute('select username,sno from user where username=%s and password=%s', [username, password])
        r = cursor.fetchone()
        if r:
            cursor.execute('select name,identify from school where sno=%s', r[1])
            rr = cursor.fetchone()
            rp['name'] = rr[0]
            if rr[1] == '学生':
                rp['identify'] = '同学'
            else: rp['identify'] = rr[1]
            return render(request, 'index.html', rp)
        else:
            rp['r'] = 'false'
            return render(request, 'login.html', rp)


