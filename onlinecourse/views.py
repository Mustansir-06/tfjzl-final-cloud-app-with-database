from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    if request.method == 'POST':
        selected_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_ids.append(int(value))
                
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
        submission.save()
        
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    grade = 0
    possible_score = 0
    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            grade += question.grade
            
    context['course'] = course
    context['grade'] = grade
    context['possible_score'] = possible_score
    context['submission'] = submission
    context['selected_ids'] = selected_ids
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
