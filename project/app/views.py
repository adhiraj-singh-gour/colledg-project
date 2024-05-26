from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .models import *
from django.contrib.auth.forms import UserCreationForm
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here


def home(request):
    obj = Course.objects.all()
    return render(request, "home.html", {"obj": obj})


def coursepage(request, slug):
    print(request.user)
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get("lecture")
    if serial_number is None:
        serial_number = 1
    video = Video.objects.get(serial_number=serial_number, course=course)
    if (request.user.is_authenticated is False) and (video.is_preview is False):
        return redirect("login")

    print(serial_number)
    context = {
        "course": course,
        "video": video,
    }
    return render(request, "course_page.html", context=context)


# user Login Signup
def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def login(request):
    return render(request, "login.html")


# client = razorpay.Client(auth=("rzp_test_ank5gb82ed6Jfx","jPpRlGXIaMvgyrlcb1gXuEoV"))


def check_out(request, slug):
    course = Course.objects.get(slug=slug)
    if not request.user.is_authenticated:
        return redirect("login")

    action = request.GET.get("action")
    if action == "create_payment":
        amount = int(
            (course.price - (course.price * course.discount * 0.01)) * 100
        )  # Convert to paise
        context = {
            "course": course,
            "amount": amount,
        }
        return render(request, "check-out.html", context=context)
    else:
        context = {
            "course": course,
        }
        return render(request, "check-out.html", context=context)


def payment(request):
    if request.method == "POST":
        # course_id = request.POST.get("course")
        # amount = request.POST.get("amount")
        amount = float(539) * 100
        print(amount)
        course = Course.objects.get(name="Html")
        if not course or not amount:
            return HttpResponseBadRequest("Course and amount are required fields.")

        try:
            client = razorpay.Client(
                auth=("rzp_test_AcIEh6rX45zRp8", "alxj2MIEOtVrhPpGGbMyFvmX")
            )
            response_payment = client.order.create(
                {
                    "amount": amount,
                    "currency": "INR",  # Use a supported currency like INR
                    "payment_capture": "1",
                }
            )
        except razorpay.errors.BadRequestError as e:
            return HttpResponseBadRequest(f"Bad Request: {str(e)}")
        except razorpay.errors.ServerError as e:
            return HttpResponse("Server Error: Please try again later.", status=500)

        order_status = response_payment["status"]
        payment_id = response_payment["id"]
        print(
            response_payment["amount"],
            response_payment["currency"],
            response_payment["id"],
        )
        if order_status == "created":
            # product = Payment(name=course.name, price=amount, payment_id=payment_id)
            # product.save()
            response_payment["name"] = course.name

            return render(request, "payment.html", {"payment": response_payment})
    else:

        return render(request, "payment.html")


@csrf_exempt
def success(request):
    # print(request.POST)
    if request.method == "POST":
        response = request.POST
        print(response)
        params_dict = {
            "razorpay_order_id": response["razorpay_order_id"],
            "razorpay_payment_id": response["razorpay_payment_id"],
            "razorpay_signature": response["razorpay_signature"],
        }

        # client instance
        client = razorpay.Client(
            auth=("rzp_test_AcIEh6rX45zRp8", "alxj2MIEOtVrhPpGGbMyFvmX")
        )

        try:
            status = client.utility.verify_payment_signature(params_dict)

            item = Payment.objects.get(Payment_id=response["razorpay_order_id"])
            item.razorpay_payment_id = response["razorpay_payment_id"]
            item.paid = True
            item.save()
            print("save all data in model")
            card = request.session["card"]
            card.clear()
            request.session["card"] = card
            print(status)
            return render(request, "success.html", {"status": True})
        except:
            print("Not save all data in model")
            return render(request, "success.html", {"status": False})

    return render(request, "success.html")
