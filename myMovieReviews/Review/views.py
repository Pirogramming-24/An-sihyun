from django.shortcuts import render, redirect, get_object_or_404
from .models import Review

def review_list(request):
    # order_by 정렬, - 있으면 내림차순
    all_reviews = Review.objects.all().order_by("-star", "-release") 
    # 별점 높은순 정렬, 별점이 같을 때 개봉년도 최신순 정렬
    return render(request, "review_list.html", {"reviews": all_reviews})

def add_a_new_review(request):
    # save 버튼 눌렀을 때
    if request.method == 'POST':
        Review.objects.create(
            title=request.POST.get('title'),
            director=request.POST.get('director'),
            actor=request.POST.get('actor'),
            release=request.POST.get('release') or 0,
            genre=request.POST.get('genre'),
            star=request.POST.get('star') or 0,
            runningtime=request.POST.get('runningtime') or 0,
            review_content=request.POST.get('review_content'),
        )
        return redirect('Review:review_list') 
    
    # save 버튼을 누르기 전까진 if문은 항상 false이므로 
    return render(request, 'review_form.html', {'review': None}) 
    # "review":None 인 이유는, 새로운 리뷰를 작성할 때 사용하는 함수이기 때문임
    # review_form.html에서 review.(title, 등등)을 하는데 새로 만들 때는 None으로 객체가 없기 때문에 default를 이용해 빈 값으로 설정
    # 기존 리뷰를 수정하는 경우는 갖고 온 객체의 각 값들을 불러와서 form을 미리 채워둠

def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if review.runningtime >=60:
        a = review.runningtime//60
        b = review.runningtime%60
        time={"time1":a, "time2":b}
    else:
        time=None

    context = {"review":review,
               "time":time}
    
    # context로 오는 딕셔너리는 한 개만 가능함.
    return render(request, "detail.html", context)

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    # save 버튼 눌렀을 때  
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.release = request.POST.get('release')
        review.genre = request.POST.get('genre')
        review.star = request.POST.get('star')
        review.runningtime = request.POST.get('runningtime')
        review.review_content = request.POST.get('review_content')
        review.director = request.POST.get('director')
        review.actor = request.POST.get('actor')
        
        # DB에 진짜 저장
        review.save() 
        return redirect('Review:detail', pk=pk)
    
    # save 버튼을 누르기 전까진 if문은 항상 false이므로 
    return render(request, 'review_form.html', {'review': review})
    # 기존 리뷰를 수정하는 경우는 갖고 온 객체의 각 값들을 불러와서 form을 미리 채워둠
    # html의 장르 선택 부분은 selected로 미리 고른 선택지를 유지해둠. 그 외는 {{review.(title, 등등)}}로 값을 불러옴.
    

def review_delete(request, pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=pk)
        
        # DB에 진짜 삭제
        review.delete()
    return redirect('Review:review_list')