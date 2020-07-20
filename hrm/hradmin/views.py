from django.shortcuts import render
from .forms import EmployeeForm, UserForm


def createemployee(request):
    if request.method == "POST":
        cu = UserForm(request.POST)
        em = EmployeeForm(request.POST)

        if cu.is_valid() and em.is_valid():
            user = cu.save(commit=False)
            user.is_staff = True
            user.save()
            emp = em.save(commit=False)
            emp.user = user
            emp.save()
            return render(request, 'home.html')
        else:
            return render(request, 'create_employee.html',{'user':cu,'employee':em})

    cu = UserForm()
    em = EmployeeForm()
    context = {'user':cu, 'employee': em}
    return render(request, 'create_employee.html', context)