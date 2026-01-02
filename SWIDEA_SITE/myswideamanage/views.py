from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import Idea, IdeaStar, DevTool
from .forms import IdeaForm, DevForm
import json
from django.http import JsonResponse
from django.db.models import Count

# ''
def idea_list(request):
    sort = request.GET.get('sort')

    # models에서 related_name='star'로 설정함 -> Count('star')로
    ideas = Idea.objects.annotate(star_opt=Count('star'))

    if sort == 'star':
        ideas = ideas.order_by('-star_opt', '-pk')
    elif sort and sort != 'default':
        ideas = ideas.order_by(sort)
    else:
        ideas = Idea.objects.all()
    
    # 찜 여부 체크 로직
    for idea in ideas:
        idea.is_starred = IdeaStar.objects.filter(idea=idea).exists()

    context = {
        'ideas': ideas,
        'sort': sort
    }
    return render(request, "myswideamanage/idea_list.html", context)

# 'idea/register/'
def idea_register(request):
    # 처음 함수가 호출되었을 때는 GET 상태 -> 빈 폼 상태
    # save 버튼 눌렀을 때 form 저장됨 -> idea_list 페이지로 감
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES) 
        # request.POST에는 사용자가 입력한 텍스트 데이터들이 담겨 있음
        # request.FILES에는 사용자가 업로드한 파일이나 이미지 데이터들이 담겨 있음
        if form.is_valid():
            form.save()
            return redirect('idea_list')
    else:
        form = IdeaForm()
        # instance가 없으므로 자동으로 '빈 폼'이 됨

    return render(request, 'myswideamanage/idea_form.html', {'form': form})

# 'idea/<int:pk>/update/'
def idea_update(request, pk):
    idea_instance = get_object_or_404(Idea, pk=pk)
   
    if request.method == 'POST':
        # 기존 데이터(instance) 위에 사용자가 새로 입력한 데이터(POST)를 덮어씀
        form = IdeaForm(request.POST, request.FILES, instance=idea_instance)
        if form.is_valid():
            form.save()
            return redirect('idea_detail', pk=pk)
    else:
        # instance를 넣어줬으므로 자동으로 '기존 내용이 채워진 폼'이 됨
        form = IdeaForm(instance=idea_instance)
    return render(request, 'myswideamanage/idea_form.html', {'form': form})

# 'idea/<int:pk>/'
def idea_detail (request, pk):
    idea=get_object_or_404(Idea,pk=pk)
    idea.is_starred = IdeaStar.objects.filter(idea=idea).exists()
    return render(request, 'myswideamanage/idea_detail.html', {'idea':idea})

# 'idea/<int:pk>/delete/'
def idea_delete (request,pk):
    if request.method == "POST":
        idea=get_object_or_404(Idea,pk=pk)
        idea.delete()
    return redirect('idea_list')



def dev_list (request):
    tools=DevTool.objects.all()
    context = {
        'tools':tools
    }
    return render(request, 'myswideamanage/devtool_list.html', context)

def dev_register (request):
    if request.method == 'POST':
        form = DevForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('dev_list')
    else:
        form = DevForm()
    return render(request, 'myswideamanage/devtool_form.html',{'form': form})

def dev_detail (request, pk):
    tool=get_object_or_404(DevTool,pk=pk)
    related_ideas = tool.ideas.all()
    return render(request, 'myswideamanage/devtool_detail.html', {'tool':tool, 'related_ideas': related_ideas})

def dev_update (request,pk):
    dev_instance = get_object_or_404(DevTool, pk=pk) 
    if request.method == 'POST':
        # 기존 데이터(instance) 위에 사용자가 새로 입력한 데이터(POST)를 덮어씀
        form = DevForm(request.POST, request.FILES, instance=dev_instance)
        if form.is_valid():
            form.save()
            return redirect('dev_detail', pk=pk)
    else:
        # instance를 넣어줬으므로 자동으로 '기존 내용이 채워진 폼'이 됨
        form = DevForm(instance=dev_instance)
    return render(request, 'myswideamanage/devtool_form.html', {'form': form})

def dev_delete (request,pk):
    if request.method=='POST':
        tool=get_object_or_404(DevTool,pk=pk)
        tool.delete()
    return redirect ('dev_list')


def star_toggle(request):
    data = json.loads(request.body)
    idea_id = data.get('id')
    idea = Idea.objects.get(id=idea_id)

    star = IdeaStar.objects.filter(idea=idea)

    if star.exists():
        star.delete()
        is_starred = False
    else:
        IdeaStar.objects.create(idea=idea)
        is_starred = True

    return JsonResponse({'is_starred': is_starred})

@csrf_exempt
def interest_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        idea_id = data.get('id')
        action = data.get('action')
        
        idea = Idea.objects.get(id=idea_id)
        
        if action == 'plus':
            idea.interest += 1
        elif action == 'minus' and idea.interest > 0: # 0보다 작아지지 않게 방어
            idea.interest -= 1
        
        idea.save()
        return JsonResponse({'interest': idea.interest}) # 바뀐 숫자를 돌려줌