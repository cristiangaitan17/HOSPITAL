from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from . import exports

# Router con versionado
router = DefaultRouter()
router.register(r'especialidades', views.EspecialidadViewSet)
router.register(r'medicos', views.MedicoViewSet)
router.register(r'pacientes', views.PacienteViewSet)
router.register(r'citas', views.CitaViewSet)
router.register(r'medicamentos', views.MedicamentoViewSet)
router.register(r'tratamientos', views.TratamientoViewSet)
router.register(r'facturas', views.FacturaViewSet)
router.register(r'pagos', views.PagoViewSet)

urlpatterns = [
    # API versionada (v1)
    path('v1/', include(router.urls)),
    
    # Autenticación JWT
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Exportaciones a Excel
    path('v1/export/especialidades/', exports.export_especialidades, name='export_especialidades'),
    path('v1/export/medicos/', exports.export_medicos, name='export_medicos'),
    path('v1/export/pacientes/', exports.export_pacientes, name='export_pacientes'),
    path('v1/export/citas/', exports.export_citas, name='export_citas'),
    path('v1/export/medicamentos/', exports.export_medicamentos, name='export_medicamentos'),
    path('v1/export/tratamientos/', exports.export_tratamientos, name='export_tratamientos'),
    path('v1/export/facturas/', exports.export_facturas, name='export_facturas'),
    path('v1/export/pagos/', exports.export_pagos, name='export_pagos'),
]