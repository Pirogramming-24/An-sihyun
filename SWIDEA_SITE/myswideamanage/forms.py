from django import forms
from .models import Idea, DevTool

# class IdeaForm(forms.ModelForm):
#     # class Meta == 모델이나 폼 그 자체에 대한 설정 정보(데이터의 데이터)를 담는 상자
#     class Meta:
#         model = Idea
#         # 사용자에게 입력받을 필드 순서
#         fields = ['title', 'image', 'content', 'interest', 'devtool']
        
#         # 각 필드에 이름을 붙이거나 스타일(클래스)을 줄 때 사용합니다.
#         labels = {
#             'title': '아이디어명',
#             'image': 'Image',
#             'content': '아이디어 설명',
#             'interest': '아이디어 관심도',
#             'devtool': '예상 개발 툴',
#         }
        
#         # HTML 태그에 직접 CSS 클래스를 넣고 싶을 때 사용합니다.
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '아이디어 제목'}),
#             'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
#             'interest': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
#             'devtool': forms.Select(attrs={'class': 'form-control'}),
#         }

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'image', 'content', 'interest', 'devtool']
        
        # 만약 기존에 'devtool' 위젯을 TextInput 등으로 고정해뒀다면 삭제하세요!
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            # 'devtool'은 장고가 자동으로 Select 위젯을 사용합니다.
        }

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        # 선택창에 '개발 툴을 선택하세요'라는 기본 문구를 넣고 싶을 때
        self.fields['devtool'].empty_label = "-- 개발 툴 선택 --"
        # 모든 필드에 일괄적으로 CSS 클래스를 넣고 싶다면 아래처럼 사용합니다.
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class DevForm(forms.ModelForm):
    class Meta:
        model = DevTool
        fields = ['name', 'kind', 'content']
        labels={
            'name' : '이름',
            'kind' : '종류',
            'content' : '개발툴 설명',
        }

        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'kind' : forms.TextInput(attrs={'class':'form-control'}),
            'content' : forms.Textarea(attrs={'class' : 'form-control'}),
        }