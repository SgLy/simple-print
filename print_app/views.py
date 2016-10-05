from django.shortcuts import render
from django.http import HttpResponse
import os

def code(request):
    return render(request, 'print_code.html')

def print_code(request):
    if request.method == 'POST':
        syntax = request.POST['syntax']
        content = request.POST['content']
        markdown = '```' + syntax + '\n' + content + '\n```'
        f = open('tmp.md', 'w')
        f.write(markdown)
        f.close()
        if os.system('pandoc tmp.md -o tmp.pdf --latex-engine=xelatex -V monofont="Monaco"') == 0:
            f = open('tmp.pdf' ,'r')
            pdf = f.read()
            f.close()
            os.system('rm tmp.md tmp.pdf')
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="code.pdf"'
            return response
        else:
            return HttpResponse('gg')


def print_webpage(request):
    return render(request, 'print_webpage.html')
