from django.http import JsonResponse
from .models import Employee
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_employee(request):

    if request.method == "POST":

        data = json.loads(request.body)

        Employee.objects.create(
            dept_id=data['deptId'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            joining_date=data['joiningDate'],
            
            city=data['city'],
            state=data['state'],
            
            contact_no=data['contact'],
            email=data['email']
        )

        return JsonResponse({"message": "Employee Added"})
    
@csrf_exempt
def search_employee(request, emp_id):

    try:

        emp = Employee.objects.get(id=emp_id)

        data = {
            "firstName": emp.first_name,
            "lastName": emp.last_name,
            "city": emp.city,
            "contact": emp.contact_no,
            "email": emp.email
        }

        return JsonResponse(data)

    except Employee.DoesNotExist:

        return JsonResponse({"error": "Employee not found"})
    
@csrf_exempt
def delete_employee(request, emp_id):

    if request.method == "DELETE":

        try:

            emp = Employee.objects.get(id=emp_id)

            emp.delete()

            return JsonResponse({"message": "Employee deleted"})

        except Employee.DoesNotExist:

            return JsonResponse({"error": "Employee not found"})    
        
def employee_home(request):
    return HttpResponse("Employee API is running")

def get_employees(request):

    employees = list(Employee.objects.values())

    return JsonResponse(employees, safe=False)