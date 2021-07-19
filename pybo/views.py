from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required


def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

# '-' 기호는 내림차순 정렬
    # return HttpResponse("안녕하세요~! Welcome!")


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')  # '@'을 데코레이터라고 함
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # 인증된 사용자(글쓴이)
            answer.question = question
            answer.create_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request):
    # 질문 등록
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # 인증된 사용자(글쓴이)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:   # request.method == 'GET'
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


def jqtest(request):
    return render(request, 'pybo/jqtest.html')


def imgtest(request):
    return render(request, 'pybo/imgtest.html')


def market(request):
    return render(request, 'pybo/market.html')


def components(request):
    return render(request, 'pybo/boot_components.html')