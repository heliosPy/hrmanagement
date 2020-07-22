from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout ,authenticate, get_user_model
from django.urls import reverse




from .forms import EmployeeForm, UserForm, AdminLoginForm
from .models import Employee



User = get_user_model()

def admin_login(request):
    """for checking the credentials of the admin who is also a super super who adds the employess"""
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email_ = form.cleaned_data["email"]
            user = User.objects.get(email__iexact=email_)
            login(request, user)
            print('this is passed as it is logined ')
            return redirect('hradmin:home')
        return render(request, 'hradmin/login.html',{'loginform':form})
    form = AdminLoginForm()
    return render(request, 'hradmin/login.html',{'loginform':form})

@login_required(login_url='/hradmin/login')
def hradminhome(request):
    return render(request, 'hradmin/home.html')

@login_required(login_url='/hradmin/login/')
def add_employee(request):
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
            return redirect('hradmin:home')
        else:
            return render(request, 'hradmin/add_emp.html',{'user':cu,'employee':em})

    cu = UserForm()
    em = EmployeeForm()
    context = {'user':cu, 'employee': em}
    return render(request, 'hradmin/add_emp.html', context)

@login_required(login_url='/hradmin/login/')
def veiw_all_emp(request):
    qs = Employee.objects.all()
    return render(request, 'hradmin/view_emp.html', {'data': qs})


@login_required(login_url='/hradmin/login')
def update_emp(request):

    qs =Employee.objects.all()
    return render(request, 'hradmin/update_emp.html',{'data':qs})

@login_required(login_url='/hradmin/login')
def ind_update(request):
    id = request.GET.get('idno') or request.POST.get('idno')
    data = Employee.objects.get(user_id=id)
    if request.method == 'POST':
        emp = EmployeeForm(request.POST, instance=data)
        # instance=data)
        # the instance is used because we need to have the old datal also
        if emp.is_valid() :
            emp.save()  # the formmodel doesnt have any update method
            messages.success(request, "Employee Updated Sucessfully")
            return redirect("hradmin:home")
        else:
            return render(request, "hradmin/update_ind.html",
                          {"employee": emp, "message": "not updated somithing is wronge"})
    emp = EmployeeForm(instance=data)
    return render(request, "hradmin/update_ind.html",
                  {"employee": emp})


@login_required(login_url='/hradmin/login/')
def del_employe(request):
    if request.method == "POST":
        dlist = request.POST.getlist('t1')
        for i in dlist:
            User.objects.get(id=i).delete()
        return redirect('hradmin:home')
    qs = Employee.objects.all()
    return render(request, 'hradmin/edelete.html',{'data':qs})


