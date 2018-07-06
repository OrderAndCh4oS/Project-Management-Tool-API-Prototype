from rest_framework import routers

from project_management.views import AddressViewSet, StatusGroupViewSet, StaffViewSet, JobViewSet, ProjectViewSet, \
    ClientViewSet, CompanyViewSet

router = routers.DefaultRouter()
router.register(r'address', AddressViewSet, base_name='address')
router.register(r'company', CompanyViewSet)
router.register(r'client', ClientViewSet, base_name='client')
router.register(r'project', ProjectViewSet)
router.register(r'job', JobViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'status-group', StatusGroupViewSet)
urlpatterns = router.urls