from rest_framework import routers

from api import views

router = routers.SimpleRouter()
router.register('v1/default-deduction', views.DefaultDeductionListFilterModelViewSet)
router.register(
    'v1/note',
    views.NoteModelListFilterModelViewSet
)
router.register(
    'v1/plan',
    views.PlanModelListFilterModelViewSet
)
router.register(
    'v1/task',
    views.TaskModelListFilterModelViewSet
)
router.register(
    'v1/user',
    views.UserViewSet
)
