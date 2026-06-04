# 🏥 Hospital API - Sistema de Gestión Hospitalaria

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![DRF](https://img.shields.io/badge/DRF-3.15-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange)
![Swagger](https://img.shields.io/badge/Swagger-Documentation-brightgreen)

## 📋 Información General

| Campo | Descripción |
|-------|-------------|
| **Nombre del proyecto** | Hospital API - Sistema de Gestión Hospitalaria |
| **Autor** | Steven Cristian Gaitán Hernández |
| **Tecnólogo** | Análisis y Desarrollo de Software - ADSO |
| **Institución** | Servicio Nacional de Aprendizaje - SENA |
| **Instructor** | Fabian David Barreto Sanchez |

### Problema Desarrollado

Una clínica requiere un sistema para administrar pacientes, médicos, especialidades, citas médicas, tratamientos, medicamentos, facturación y pagos. La API desarrollada permite gestionar de manera eficiente todas estas operaciones a través de endpoints RESTful, garantizando seguridad mediante autenticación JWT y siguiendo buenas prácticas de desarrollo.

### Tablas Implementadas

| # | Tabla | Descripción |
|---|-------|-------------|
| 1 | Especialidades | Catálogo de especialidades médicas |
| 2 | Médicos | Personal médico asociado a especialidades |
| 3 | Pacientes | Registro de pacientes |
| 4 | Citas | Programación de citas médicas |
| 5 | Medicamentos | Inventario de medicamentos |
| 6 | Tratamientos | Tratamientos asociados a citas |
| 7 | Facturas | Facturación de servicios |
| 8 | Pagos | Registro de pagos realizados |

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.13 | Lenguaje principal |
| **Django** | 6.0 | Framework web |
| **Django REST Framework** | 3.15 | API REST |
| **PostgreSQL** | 15 | Base de datos |
| **JWT** | - | Autenticación |
| **drf-yasg** | - | Documentación Swagger |
| **openpyxl** | - | Exportación a Excel |
| **python-dotenv** | - | Variables de entorno |

### Características Implementadas

- ✅ Swagger para documentación
- ✅ Versionado de API (v1)
- ✅ Respuestas JSON estandarizadas
- ✅ Paginación
- ✅ Filtros y ordenamiento
- ✅ Soft Delete
- ✅ Auditoría de registros
- ✅ Autenticación JWT
- ✅ Roles y permisos
- ✅ Relaciones anidadas (Nested Serializers)
- ✅ Exportación a Excel/CSV
- ✅ Logging de operaciones

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/cristiangaitan17/HOSPITAL.git
cd HOSPITAL
