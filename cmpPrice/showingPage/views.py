from django.shortcuts import render
from .spider.jdPro import jdSearch
from .spider.taobaoPro import tbSearch
from .spider.zggjtsg import bookdetails
from .spider.amazon import amazon
from .spider.dangdang import dangdang
# Create your views here.

def home(request):
    try:
        input = request.POST.get('search')
    except:
        input='python'
    if not input:
        context = {'JD_goodslist': [], 'TB_goodslist':[]}
        return render(request,'showingPage/home.html',context)

    try:
        n = int(request.POST.get('number'))
    except:
        n=10
    if n<=0:
        n=10

    jd=jdSearch(input,n)
    tb=tbSearch(input,n)
    context={'JD_goodslist':jd,'TB_goodslist':tb}
    return render(request,'showingPage/home.html',context)

def cmpPrice(request,id):
    jd = jdSearch(id,5)
    a=amazon(id)
    dd=dangdang(id)
    imgs=a[0]['good_pic']
    if imgs==None:
        imgs=jd[0]['good_pic']
    s=bookdetails(id)
    [name, author, publisher, abstract]=s
    result=a+jd+dd
    context = {'result': result,
               'publisher':publisher,
               'ISBN':id,
               'name':name,
               'author':author,
               'abstract':abstract,
               'imgs':imgs
               }
    return render(request, 'showingPage/book_detail.html', context)