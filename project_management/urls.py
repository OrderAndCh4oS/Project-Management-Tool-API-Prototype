from rest_framework import routers

from project_management import views

router = routers.DefaultRouter()
router.register(r'register', views.CreateUserViewSet, base_name='register')
router.register(r'staff', views.StaffViewSet)
router.register(r'address', views.AddressViewSet, base_name='address')
router.register(r'email-address', views.EmailAddressViewSet, base_name='email-address')
router.register(r'client', views.ClientViewSet, base_name='client')
router.register(r'company', views.CompanyViewSet)
router.register(r'status-group', views.StatusGroupViewSet)
router.register(r'status', views.StatusViewSet)
router.register(r'project', views.ProjectViewSet)
router.register(r'job', views.JobViewSet)
router.register(r'task', views.TaskViewSet)
router.register(r'work-day', views.WorkDayViewSet)
router.register(r'scheduled-todo', views.ScheduledTodoViewSet)
urlpatterns = router.urls
