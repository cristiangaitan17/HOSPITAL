from rest_framework import serializers
from django.db import models
from .models import (
    Especialidad, Medico, Paciente, Cita,
    Medicamento, Tratamiento, Factura, Pago
)


# ============================================
# 1. ESPECIALIDADES
# ============================================
class EspecialidadSerializer(serializers.ModelSerializer):
    total_medicos = serializers.IntegerField(source='medicos.count', read_only=True)
    
    class Meta:
        model = Especialidad
        fields = '__all__'


# ============================================
# 2. MEDICOS (con relación anidada a Especialidad)
# ============================================
class MedicoSerializer(serializers.ModelSerializer):
    especialidad_nombre = serializers.ReadOnlyField(source='especialidad.nombre')
    especialidad_detalle = EspecialidadSerializer(source='especialidad', read_only=True)
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Medico
        fields = '__all__'
    
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"


# ============================================
# 3. PACIENTES
# ============================================
class PacienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    edad = serializers.SerializerMethodField()
    
    class Meta:
        model = Paciente
        fields = '__all__'
    
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    
    def get_edad(self, obj):
        from datetime import date
        if obj.fecha_nacimiento:
            today = date.today()
            return today.year - obj.fecha_nacimiento.year - (
                (today.month, today.day) < (obj.fecha_nacimiento.month, obj.fecha_nacimiento.day)
            )
        return None


# ============================================
# 4. CITAS (con relaciones anidadas a Paciente y Medico)
# ============================================
class CitaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.ReadOnlyField(source='paciente.nombre_completo')
    medico_nombre = serializers.ReadOnlyField(source='medico.nombre_completo')
    paciente_detalle = PacienteSerializer(source='paciente', read_only=True)
    medico_detalle = MedicoSerializer(source='medico', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Cita
        fields = '__all__'


# ============================================
# 5. MEDICAMENTOS
# ============================================
class MedicamentoSerializer(serializers.ModelSerializer):
    disponible = serializers.BooleanField(source='stock > 0', read_only=True)
    
    class Meta:
        model = Medicamento
        fields = '__all__'


# ============================================
# 6. TRATAMIENTOS (con relaciones anidadas a Cita y Medicamento)
# ============================================
class TratamientoSerializer(serializers.ModelSerializer):
    cita_fecha = serializers.ReadOnlyField(source='cita.fecha_hora')
    medicamento_nombre = serializers.ReadOnlyField(source='medicamento.nombre')
    paciente_nombre = serializers.ReadOnlyField(source='cita.paciente.nombre_completo')
    
    class Meta:
        model = Tratamiento
        fields = '__all__'


# ============================================
# 7. FACTURAS (con relación anidada a Paciente)
# ============================================
class FacturaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.ReadOnlyField(source='paciente.nombre_completo')
    total_pagado = serializers.SerializerMethodField()
    saldo_pendiente = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Factura
        fields = '__all__'
    
    def get_total_pagado(self, obj):
        total = obj.pagos.filter(activo=True).aggregate(total=models.Sum('monto'))['total']
        return float(total) if total else 0
    
    def get_saldo_pendiente(self, obj):
        pagado = self.get_total_pagado(obj)
        return float(obj.total) - pagado


# ============================================
# 8. PAGOS (con relación anidada a Factura)
# ============================================
class PagoSerializer(serializers.ModelSerializer):
    factura_paciente = serializers.ReadOnlyField(source='factura.paciente.nombre_completo')
    factura_total = serializers.ReadOnlyField(source='factura.total')
    metodo_display = serializers.CharField(source='get_metodo_pago_display', read_only=True)
    
    class Meta:
        model = Pago
        fields = '__all__'