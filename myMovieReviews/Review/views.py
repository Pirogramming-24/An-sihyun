from django.shortcuts import render, redirect, get_object_or_404
from .models import Review

# 1. 리뷰 리스트
def review_list(request):
    all_reviews = Review.objects.all()
    return render(request, "review_list.html", {"reviews": all_reviews})

# 2. 새 리뷰 작성 (Create)
def add_a_new_review(request):
    if request.method == 'POST':
        Review.objects.create(
            title=request.POST.get('title'),
            director=request.POST.get('director'),
            actor=request.POST.get('actor'),  # actor로 수정 완료!
            release=request.POST.get('release') or 0,
            genre=request.POST.get('genre'),
            star=request.POST.get('star') or 0,
            runningtime=request.POST.get('runningtime') or 0,
            review_content=request.POST.get('review_content'),
        )
        return redirect('Review:review_list') 
    
    return render(request, 'review_form.html', {'review': None})

# 3. 리뷰 상세
def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, "detail.html", {"review": review})

# 4. 리뷰 수정 (Update)
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.release = request.POST.get('release') or 0
        review.genre = request.POST.get('genre')
        review.star = request.POST.get('star') or 0
        review.runningtime = request.POST.get('runningtime') or 0
        review.review_content = request.POST.get('review_content')
        review.director = request.POST.get('director')
        review.actor = request.POST.get('actor') # actor로 수정 완료!
        
        review.save() 
        return redirect('Review:detail', pk=pk)
    
    return render(request, 'review_form.html', {'review': review})
    

# 5. 리뷰 삭제 (Delete)
def review_delete(request, pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=pk)
        review.delete()
    return redirect('Review:review_list')