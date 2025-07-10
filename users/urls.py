from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserViewSet, UserCreateAPIView
from django.urls import path
from users.views import PaymentListView, PaymentDetailView, PaymentCreateView, PaymentUpdateView, PaymentDeleteView

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
                  path('register/', UserCreateAPIView.as_view(), name='register'),
                  path('login/', TokenObtainPairView.as_view(), name='login'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

                  path('payments/', PaymentListView.as_view(), name='payment-list'),
                  path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
                  path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
                  path('payments/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment-update'),
                  path('payments/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment-delete'),
              ] + router.urls
