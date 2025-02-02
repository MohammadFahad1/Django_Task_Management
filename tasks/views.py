from django.shortcuts import render
# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
        "name": ["Mahmud", "Ahmed", "John"],
        "Fahad": {"name": "Md. Fahad Monshi", "eye": "blue"}
    }
    return render(request, "test.html", context)