from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('review/',views.submit_review,name='submit_review'),
    path('thank-you/',views.thank_you,name='thank_you'),
    path('admin-login/',views.admin_login,name='admin_login'),
    path('admin-logout/',views.admin_logout,name='admin_logout'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('google/login/',views.google_login,name='google_login'),
    path('google/callback/',views.google_callback,name='google_callback'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('review/<int:review_id>/',views.review_detail,name='review_detail'),
    path('export/reviews/csv/',views.export_reviews_csv,name='export_reviews_csv'),
    path('export/reviews/excel/',views.export_reviews_excel,name='export_reviews_excel'),
    path('manage-profile/',views.manage_profile,name='manage_profile'),
]