from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InterviewQuestion, PracticeSession


def question_bank(request):
    questions = InterviewQuestion.objects.all()
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    role = request.GET.get('role', '')
    company_id = request.GET.get('company', '')
    q = request.GET.get('q', '')

    if category:
        questions = questions.filter(category=category)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)
    if role:
        questions = questions.filter(role_tag__icontains=role)
    if company_id:
        questions = questions.filter(company_id=company_id)
    if q:
        questions = questions.filter(question__icontains=q)

    companies = InterviewQuestion.objects.exclude(company__isnull=True).values('company__company_name', 'company__id').distinct()
    companies_list = [ {'id': c['company__id'], 'name': c['company__company_name']} for c in companies ] + [{'id': '', 'name': 'All Companies / Global'}]

    return render(request, 'interviews/question_bank.html', {
        'questions': questions,
        'CATEGORIES': InterviewQuestion.CATEGORY,
        'DIFFICULTIES': InterviewQuestion.DIFFICULTY,
        'COMPANIES': companies_list,
        'selected_category': category,
        'selected_difficulty': difficulty,
        'selected_company': company_id,
        'role': role,
        'q': q,
    })


def company_interview_prep(request, company_pk):
    """Interview prep section on a company's profile — visible to all."""
    from accounts.models import CompanyProfile
    company = get_object_or_404(CompanyProfile, pk=company_pk)
    questions = InterviewQuestion.objects.filter(company=company)
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    if category:
        questions = questions.filter(category=category)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)
    return render(request, 'interviews/company_prep.html', {
        'company': company,
        'questions': questions,
        'CATEGORIES': InterviewQuestion.CATEGORY,
        'DIFFICULTIES': InterviewQuestion.DIFFICULTY,
        'selected_category': category,
        'selected_difficulty': difficulty,
    })


@login_required
def practice(request, pk):
    if not request.user.is_jobseeker():
        messages.error(request, "Only job seekers can practice.")
        return redirect('question_bank')
    question = get_object_or_404(InterviewQuestion, pk=pk)
    session = None
    if request.method == 'POST':
        user_answer = request.POST.get('user_answer', '').strip()
        if user_answer:
            answer_words = set(user_answer.lower().split())
            sample_words = set(question.sample_answer.lower().split())
            common = answer_words.intersection(sample_words)
            score = min(100, int((len(common) / max(len(sample_words), 1)) * 100))

            session = PracticeSession.objects.create(
                seeker=request.user.seeker_profile,
                question=question,
                user_answer=user_answer,
                score=score,
                feedback=generate_feedback(score)
            )
    return render(request, 'interviews/practice.html', {
        'question': question,
        'session': session,
    })


def generate_feedback(score):
    if score >= 80:
        return "Excellent! Your answer covers most of the key points. You're well-prepared for this question."
    elif score >= 60:
        return "Good effort! Consider adding more specific examples and elaborating on key concepts."
    elif score >= 40:
        return "Fair attempt. Review the sample answer and try to incorporate more relevant keywords and ideas."
    else:
        return "Keep practicing! Study the sample answer carefully and try to understand the key concepts being asked."


@login_required
def my_practice_history(request):
    if not request.user.is_jobseeker():
        return redirect('question_bank')
    sessions = request.user.seeker_profile.practice_sessions.select_related('question').all()
    avg_score = 0
    if sessions.exists():
        avg_score = int(sum(s.score for s in sessions) / sessions.count())
    return render(request, 'interviews/history.html', {
        'sessions': sessions,
        'avg_score': avg_score,
    })
