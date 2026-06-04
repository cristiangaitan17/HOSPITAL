import os
import django
import random
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import (
    Especialidad, Medico, Paciente, Cita,
    Medicamento, Tratamiento, Factura, Pago
)
from faker import Faker

fake = Faker('es_ES')  # Datos en español

def crear_especialidades(n=50):
    """Crear n especialidades"""
    especialidades = []
    especialidades_existentes = [
        "Cardiología", "Neurología", "Pediatría", "Ginecología", 
        "Traumatología", "Dermatología", "Oftalmología", "Psiquiatría",
        "Oncología", "Urología", "Neumología", "Reumatología",
        "Endocrinología", "Nefrología", "Hematología", "Infectología",
        "Geriatría", "Medicina Interna", "Cirugía General", "Anestesiología"
    ]
    
    for i in range(n):
        if i < len(especialidades_existentes):
            nombre = especialidades_existentes[i]
        else:
            nombre = fake.unique.word().capitalize() + "logía"
        
        especialidad = Especialidad(
            nombre=nombre,
            descripcion=fake.text(max_nb_chars=200),
            activo=True
        )
        especialidades.append(especialidad)
    
    Especialidad.objects.bulk_create(especialidades)
    print(f"✅ Creadas {n} especialidades")
    return Especialidad.objects.all()

def crear_medicos(n=50):
    """Crear n médicos"""
    especialidades = list(Especialidad.objects.all())
    medicos = []
    
    for i in range(n):
        medico = Medico(
            especialidad=random.choice(especialidades),
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            telefono=fake.phone_number()[:15],
            email=fake.email(),
            activo=True
        )
        medicos.append(medico)
    
    Medico.objects.bulk_create(medicos)
    print(f"✅ Creados {n} médicos")
    return Medico.objects.all()

def crear_pacientes(n=50):
    """Crear n pacientes"""
    pacientes = []
    
    for i in range(n):
        # Fecha de nacimiento entre 18 y 80 años
        fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=80)
        
        paciente = Paciente(
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            cedula=fake.unique.numerify(text='##########'),
            fecha_nacimiento=fecha_nacimiento,
            telefono=fake.phone_number()[:15],
            email=fake.email(),
            direccion=fake.address(),
            activo=True
        )
        pacientes.append(paciente)
    
    Paciente.objects.bulk_create(pacientes)
    print(f"✅ Creados {n} pacientes")
    return Paciente.objects.all()

def crear_medicamentos(n=50):
    """Crear n medicamentos"""
    medicamentos_lista = [
        "Paracetamol", "Ibuprofeno", "Amoxicilina", "Losartán", "Metformina",
        "Omeprazol", "Salbutamol", "Loratadina", "Azitromicina", "Dexametasona",
        "Enalapril", "Simvastatina", "Naproxeno", "Clonazepam", "Fluoxetina",
        "Ciprofloxacino", "Diclofenaco", "Hidroclorotiazida", "Levotiroxina", "Warfarina",
        "Amlodipino", "Carvedilol", "Espironolactona", "Furosemida", "Gabapentina"
    ]
    
    medicamentos = []
    for i in range(n):
        if i < len(medicamentos_lista):
            nombre = medicamentos_lista[i]
        else:
            nombre = fake.word().capitalize()
        
        medicamento = Medicamento(
            nombre=nombre,
            descripcion=fake.sentence(),
            precio=round(random.uniform(5.0, 500.0), 2),
            stock=random.randint(0, 1000),
            activo=True
        )
        medicamentos.append(medicamento)
    
    Medicamento.objects.bulk_create(medicamentos)
    print(f"✅ Creados {n} medicamentos")
    return Medicamento.objects.all()

def crear_citas(n=50):
    """Crear n citas"""
    pacientes = list(Paciente.objects.all())
    medicos = list(Medico.objects.all())
    estados = ['pendiente', 'confirmada', 'cancelada', 'completada']
    citas = []
    
    for i in range(n):
        fecha_hora = fake.date_time_between(start_date='-30d', end_date='+60d')
        
        cita = Cita(
            paciente=random.choice(pacientes),
            medico=random.choice(medicos),
            fecha_hora=fecha_hora,
            estado=random.choice(estados),
            motivo=fake.sentence(),
            activo=True
        )
        citas.append(cita)
    
    Cita.objects.bulk_create(citas)
    print(f"✅ Creadas {n} citas")
    return Cita.objects.all()

def crear_tratamientos(n=50):
    """Crear n tratamientos"""
    citas = list(Cita.objects.filter(activo=True))
    medicamentos = list(Medicamento.objects.filter(activo=True))
    tratamientos = []
    
    for i in range(n):
        if not citas or not medicamentos:
            break
        
        tratamiento = Tratamiento(
            cita=random.choice(citas),
            medicamento=random.choice(medicamentos),
            descripcion=fake.sentence(),
            dosis=f"{random.randint(1, 3)} {random.choice(['mg', 'g', 'ml', 'tableta'])}",
            duracion_dias=random.randint(1, 30),
            activo=True
        )
        tratamientos.append(tratamiento)
    
    Tratamiento.objects.bulk_create(tratamientos)
    print(f"✅ Creados {len(tratamientos)} tratamientos")
    return Tratamiento.objects.all()

def crear_facturas(n=50):
    """Crear n facturas"""
    pacientes = list(Paciente.objects.all())
    estados = ['pendiente', 'pagada', 'anulada']
    facturas = []
    
    for i in range(n):
        subtotal = round(random.uniform(50.0, 2000.0), 2)
        iva = round(subtotal * 0.19, 2)
        total = round(subtotal + iva, 2)
        
        factura = Factura(
            paciente=random.choice(pacientes),
            subtotal=subtotal,
            iva=iva,
            total=total,
            estado=random.choice(estados),
            activo=True
        )
        facturas.append(factura)
    
    Factura.objects.bulk_create(facturas)
    print(f"✅ Creadas {n} facturas")
    return Factura.objects.all()

def crear_pagos(n=50):
    """Crear n pagos"""
    facturas = list(Factura.objects.filter(activo=True, estado='pendiente'))
    metodos = ['efectivo', 'tarjeta', 'transferencia']
    pagos = []
    
    for i in range(n):
        if not facturas:
            break
        
        factura = random.choice(facturas)
        monto = float(factura.total) if factura.total else 100.0
        
        pago = Pago(
            factura=factura,
            monto=round(monto, 2),
            metodo_pago=random.choice(metodos),
            referencia=fake.unique.numerify(text='REF-########'),
            activo=True
        )
        pagos.append(pago)
        
        # Actualizar estado de factura a pagada
        factura.estado = 'pagada'
        factura.save()
    
    Pago.objects.bulk_create(pagos)
    print(f"✅ Creados {len(pagos)} pagos")
    return Pago.objects.all()

def crear_todos_los_datos():
    """Ejecutar todas las inserciones"""
    print("\n" + "="*50)
    print("🚀 INICIANDO INSERCIÓN MASIVA DE DATOS")
    print("="*50 + "\n")
    
    # Crear en orden (respetando dependencias)
    especialidades = crear_especialidades(50)
    medicos = crear_medicos(50)
    pacientes = crear_pacientes(50)
    medicamentos = crear_medicamentos(50)
    citas = crear_citas(50)
    tratamientos = crear_tratamientos(50)
    facturas = crear_facturas(50)
    pagos = crear_pagos(50)
    
    print("\n" + "="*50)
    print("✅ INSERCIÓN COMPLETADA")
    print("="*50)
    
    # Resumen
    print(f"\n📊 RESUMEN FINAL:")
    print(f"   Especialidades: {Especialidad.objects.count()}")
    print(f"   Médicos: {Medico.objects.count()}")
    print(f"   Pacientes: {Paciente.objects.count()}")
    print(f"   Medicamentos: {Medicamento.objects.count()}")
    print(f"   Citas: {Cita.objects.count()}")
    print(f"   Tratamientos: {Tratamiento.objects.count()}")
    print(f"   Facturas: {Factura.objects.count()}")
    print(f"   Pagos: {Pago.objects.count()}")

if __name__ == "__main__":
    crear_todos_los_datos()