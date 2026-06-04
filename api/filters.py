import django_filters
from .models import Especialidad, Medico, Paciente, Cita, Medicamento, Tratamiento, Factura, Pago

class EspecialidadFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Especialidad
        fields = ['nombre', 'activo']


class MedicoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    apellido = django_filters.CharFilter(lookup_expr='icontains')
    especialidad = django_filters.NumberFilter(field_name='especialidad__id')
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Medico
        fields = ['nombre', 'apellido', 'especialidad', 'activo']


class PacienteFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    apellido = django_filters.CharFilter(lookup_expr='icontains')
    cedula = django_filters.CharFilter(lookup_expr='icontains')
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'cedula', 'activo']


class CitaFilter(django_filters.FilterSet):
    paciente = django_filters.NumberFilter()
    medico = django_filters.NumberFilter()
    estado = django_filters.CharFilter(lookup_expr='iexact')
    fecha_desde = django_filters.DateFilter(field_name='fecha_hora', lookup_expr='gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha_hora', lookup_expr='lte')
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'estado', 'fecha_desde', 'fecha_hasta', 'activo']


class MedicamentoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    stock_min = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Medicamento
        fields = ['nombre', 'precio_min', 'precio_max', 'stock_min', 'activo']


class TratamientoFilter(django_filters.FilterSet):
    cita = django_filters.NumberFilter()
    medicamento = django_filters.NumberFilter()
    duracion_dias_min = django_filters.NumberFilter(field_name='duracion_dias', lookup_expr='gte')
    duracion_dias_max = django_filters.NumberFilter(field_name='duracion_dias', lookup_expr='lte')
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Tratamiento
        fields = ['cita', 'medicamento', 'duracion_dias_min', 'duracion_dias_max', 'activo']


class FacturaFilter(django_filters.FilterSet):
    paciente = django_filters.NumberFilter()
    estado = django_filters.CharFilter(lookup_expr='iexact')
    fecha_desde = django_filters.DateFilter(field_name='fecha_emision', lookup_expr='gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha_emision', lookup_expr='lte')
    total_min = django_filters.NumberFilter(field_name='total', lookup_expr='gte')
    total_max = django_filters.NumberFilter(field_name='total', lookup_expr='lte')
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Factura
        fields = ['paciente', 'estado', 'fecha_desde', 'fecha_hasta', 'total_min', 'total_max', 'activo']


class PagoFilter(django_filters.FilterSet):
    factura = django_filters.NumberFilter()
    metodo_pago = django_filters.CharFilter(lookup_expr='iexact')
    fecha_desde = django_filters.DateFilter(field_name='fecha_pago', lookup_expr='gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha_pago', lookup_expr='lte')
    monto_min = django_filters.NumberFilter(field_name='monto', lookup_expr='gte')
    monto_max = django_filters.NumberFilter(field_name='monto', lookup_expr='lte')
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Pago
        fields = ['factura', 'metodo_pago', 'fecha_desde', 'fecha_hasta', 'monto_min', 'monto_max', 'activo']