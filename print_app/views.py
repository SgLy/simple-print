from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import os, datetime

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'error': False})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': True})

@login_required
def code(request):
    if request.method == 'GET':
        return render(request, 'code.html', {'teamname': request.user.last_name})
    elif request.method == 'POST':
        syntax = request.POST['syntax']
        content = request.POST['content']
        posi = request.user.email
        if len(content) > 4096:
            return render(request, 'msg.html', {'color': '#e74c3c', 'msg': 'Your code is too long!'})
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        markdown = '# SYSU Novice Programming Contest 2016\n'
        markdown += '## Printed by %s (%s)\n' % (request.user.last_name.replace('\\', '\\\\').replace('%', '\%'), request.user.username)
        markdown += '## Print time: %s\n' % time
        markdown += '## Location: %s\n\n' % posi
        markdown += '```' + syntax + '\n' + content + '\n\n\n\n\n\n\n\n```'
        time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        with open('tmp-%s.md' % time, 'w') as f:
            f.write(markdown.encode('utf-8'))
        if os.system('pandoc tmp-%s.md -o tmp-%s.pdf --listings --latex-engine=xelatex -H listing.tex -V monofont="Courier New" -V margin-top="2cm" -V margin-down="2cm" -V margin-left="2cm" -V margin-right="2cm"' % (time, time)) == 0:
            print '--------------------------------------------------------------------'
            print '[PRINT] %s' % time
            print '--------------------------------------------------------------------'
            os.system('lpr tmp-%s.pdf -o media=a4 -o scaling=100' % time)
            # os.system('rm tmp-%s.pdf' % time)
            return render(request, 'msg.html', {'color': '#2ecc71', 'msg': 'Your code has been sent to the printer.'})

            # with open('tmp-%s.pdf' % time ,'r') as f:
            #    pdf = f.read()
            # response = HttpResponse(pdf, content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="code.pdf"'
            # return response
        else:
            return render(request, 'msg.html', {'color': '#e74c3c', 'msg': 'Some error occured! Please contact us!'})


def web(request):
    return render(request, 'webpage.html')

def print_web(request):
    if request.method == 'POST':
        url = request.POST['url'].split('\n')
        piece = int(request.POST['piece'])
        res = ''
        for t in range(piece):
            for i in url:
                res += 'print ' + i + '<br/>'
        return HttpResponse(res)
