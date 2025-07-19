import stripe
from django.conf import settings

from lms.models import Course, Lesson

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_price(amount, product_info):
    """Create a Stripe price."""
    print(product_info)
    return stripe.Price.create(
        currency="EUR",
        unit_amount=amount * 100,  # Stripe expects the amount in cents
        product_data={"name": product_info},
    )


def create_session(price):
    """Create a Stripe checkout session."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def retrieve_checkout_session(session_id):
    """Retrieve a Stripe checkout session."""
    session = stripe.checkout.Session.retrieve(
        session_id
    )
    payment_type = next(iter(session.get("payment_method_options", {})), None) if session else None
    payment_status = session.get("status", None) if session else None
    return payment_type, payment_status


def product(course, lesson):
    course_name = Course.objects.get(id=course.id).name if course else None
    lesson_name = Lesson.objects.get(id=lesson.id).name if lesson else None
    if course_name and lesson_name:
        product_name = f"{course_name} - {lesson_name}"
        return product_name
    else:
        return course.name if course else lesson.name
