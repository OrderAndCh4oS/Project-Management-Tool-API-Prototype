from rest_framework import routers

from project_management import views

router = routers.DefaultRouter()
router.register(r'register', views.CreateUserViewSet, base_name='register')
router.register(r'address', views.AddressViewSet, base_name='address')
router.register(r'company', views.CompanyViewSet)
router.register(r'client', views.ClientViewSet, base_name='client')
router.register(r'email-address', views.EmailAddressViewSet, base_name='email-address')
router.register(r'project', views.ProjectViewSet)
router.register(r'job', views.JobViewSet)
router.register(r'staff', views.StaffViewSet)
router.register(r'status-group', views.StatusGroupViewSet)
urlpatterns = router.urls