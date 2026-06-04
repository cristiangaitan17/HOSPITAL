import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Especialidad, Medico, Paciente, Cita,
    Medicamento, Tratamiento, Factura, Pago
)
from .serializers import (
    EspecialidadSerializer, MedicoSerializer, PacienteSerializer,
    CitaSerializer, MedicamentoSerializer, TratamientoSerializer,
    FacturaSerializer, PagoSerializer
)
from .pagination import CustomPagination
from .filters import (
    EspecialidadFilter, MedicoFilter, PacienteFilter, CitaFilter
)
from .permissions import IsAdminOrReadOnly, IsMedicoOrAdmin, IsPacienteOrAdmin
from .logging_utils import log_operation

# Configurar logger
logger = logging.getLogger(__name__)


# ============================================
# CLASE BASE CON SOFT DELETE Y RESPUESTAS JSON
# ============================================
class BaseViewSet(viewsets.ModelViewSet):
    """ViewSet base con soft delete, respuestas JSON y logging"""
    
    # Configuración de filtros y ordenamiento
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Solo muestra registros activos"""
        return self.queryset.filter(activo=True)
    
    def list(self, request):
        """Listar registros con paginación, filtros y ordenamiento"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'status': 200,
            'version': 'v1',
            'message': 'Petición exitosa',
            'data': serializer.data
        })
    
    def create(self, request):
        """Crear registro y loggear operación"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            # Loggear operación de creación
            log_operation(
                user=request.user,
                action='CREATE',
                model=self.queryset.model.__name__,
                object_id=instance.id,
                details=request.data
            )
            logger.info(f"CREATED: {self.queryset.model.__name__} ID={instance.id}")
            return Response({
                'success': True,
                'status': 201,
                'version': 'v1',
                'message': 'Registro creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': 400,
            'version': 'v1',
            'message': 'Error de validación',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Obtener registro por ID (incluye inactivos)"""
        try:
            instance = self.queryset.model.objects.get(pk=pk)
            serializer = self.get_serializer(instance)
            logger.info(f"RETRIEVE: {self.queryset.model.__name__} ID={pk}")
            return Response({
                'success': True,
                'status': 200,
                'version': 'v1',
                'message': 'Petición exitosa',
                'data': serializer.data
            })
        except self.queryset.model.DoesNotExist:
            return Response({
                'success': False,
                'status': 404,
                'version': 'v1',
                'message': 'Registro no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Actualizar registro y loggear operación"""
        try:
            instance = self.queryset.model.objects.get(pk=pk)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Loggear operación de actualización
                log_operation(
                    user=request.user,
                    action='UPDATE',
                    model=self.queryset.model.__name__,
                    object_id=instance.id,
                    details=request.data
                )
                logger.info(f"UPDATED: {self.queryset.model.__name__} ID={pk}")
                return Response({
                    'success': True,
                    'status': 200,
                    'version': 'v1',
                    'message': 'Registro actualizado exitosamente',
                    'data': serializer.data
                })
            return Response({
                'success': False,
                'status': 400,
                'version': 'v1',
                'message': 'Error de validación',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.model.DoesNotExist:
            return Response({
                'success': False,
                'status': 404,
                'version': 'v1',
                'message': 'Registro no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        """Soft delete: solo cambia activo a False y loggea"""
        try:
            instance = self.queryset.model.objects.get(pk=pk)
            instance.activo = False
            instance.save()
            # Loggear operación de eliminación (soft delete)
            log_operation(
                user=request.user,
                action='SOFT_DELETE',
                model=self.queryset.model.__name__,
                object_id=instance.id,
                details={'activo': False}
            )
            logger.info(f"SOFT_DELETE: {self.queryset.model.__name__} ID={pk}")
            return Response({
                'success': True,
                'status': 200,
                'version': 'v1',
                'message': 'Registro desactivado exitosamente'
            })
        except self.queryset.model.DoesNotExist:
            return Response({
                'success': False,
                'status': 404,
                'version': 'v1',
                'message': 'Registro no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)


# ============================================
# 1. ESPECIALIDADES
# ============================================
class EspecialidadViewSet(BaseViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    filterset_class = EspecialidadFilter
    search_fields = ['nombre']
    ordering_fields = ['id', 'nombre', 'fecha_creacion']
    ordering = ['id']
    permission_classes = [IsAdminOrReadOnly]


# ============================================
# 2. MEDICOS
# ============================================
class MedicoViewSet(BaseViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filterset_class = MedicoFilter
    search_fields = ['nombre', 'apellido', 'email']
    ordering_fields = ['id', 'nombre', 'apellido', 'especialidad__nombre']
    ordering = ['id']
    permission_classes = [IsMedicoOrAdmin]


# ============================================
# 3. PACIENTES
# ============================================
class PacienteViewSet(BaseViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filterset_class = PacienteFilter
    search_fields = ['nombre', 'apellido', 'cedula', 'email']
    ordering_fields = ['id', 'nombre', 'apellido', 'cedula']
    ordering = ['id']
    permission_classes = [IsAuthenticated]


# ============================================
# 4. CITAS
# ============================================
class CitaViewSet(BaseViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    filterset_class = CitaFilter
    search_fields = ['estado', 'motivo']
    ordering_fields = ['id', 'fecha_hora', 'estado']
    ordering = ['-fecha_hora']
    permission_classes = [IsAuthenticated]


# ============================================
# 5. MEDICAMENTOS
# ============================================
class MedicamentoViewSet(BaseViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    search_fields = ['nombre']
    ordering_fields = ['id', 'nombre', 'precio', 'stock']
    ordering = ['id']
    permission_classes = [IsAdminOrReadOnly]


# ============================================
# 6. TRATAMIENTOS
# ============================================
class TratamientoViewSet(BaseViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
    search_fields = ['dosis', 'descripcion']
    ordering_fields = ['id', 'duracion_dias']
    ordering = ['id']
    permission_classes = [IsMedicoOrAdmin]


# ============================================
# 7. FACTURAS
# ============================================
class FacturaViewSet(BaseViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    search_fields = ['estado']
    ordering_fields = ['id', 'fecha_emision', 'total', 'estado']
    ordering = ['-fecha_emision']
    permission_classes = [IsAuthenticated]


# ============================================
# 8. PAGOS
# ============================================
class PagoViewSet(BaseViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    search_fields = ['metodo_pago', 'referencia']
    ordering_fields = ['id', 'fecha_pago', 'monto', 'metodo_pago']
    ordering = ['-fecha_pago']
    permission_classes = [IsAuthenticated]