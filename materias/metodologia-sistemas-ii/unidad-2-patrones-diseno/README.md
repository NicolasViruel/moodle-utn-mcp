# Metodología de Sistemas II – Unidad 2: Patrones de Diseño

**Curso Moodle:** Metodología de Sistemas II (id 52)  
**Alumno:** Nicolás Viruel

## Estructura

```
unidad-2-patrones-diseno/
├── actividad-1/          PDF teórico Actividad 1
├── tp1-factory-method/   TP creacionales + entrega
├── tp2-adapter/          TP estructurales + entrega
├── tp3-observer/         TP comportamiento + entrega
└── build_pdf.py          Genera PDF desde .md
```

## Trabajos prácticos

| TP | Patrón | Entrega Moodle | Archivo a subir |
|----|--------|----------------|-----------------|
| 1 | Factory Method | Entrega práctico 1 | `tp1-factory-method/tp1-resuelto_Nicolas_Viruel.pdf` |
| 2 | Adapter | Entrega Practico 2 | `tp2-adapter/tp2-resuelto_Nicolas_Viruel.pdf` |
| 3 | Observer | Entrega práctico 3 | `tp3-observer/tp3-resuelto_Nicolas_Viruel.pdf` |

Cada entrega PDF incluye: diagrama UML antes/después, código refactorizado, justificación y pruebas.

## Ejecutar código (Python)

```powershell
python materias/metodologia-sistemas-ii/unidad-2-patrones-diseno/tp1-factory-method/factory_method_Nicolas_Viruel.py
python materias/metodologia-sistemas-ii/unidad-2-patrones-diseno/tp2-adapter/geo_adapter_Nicolas_Viruel.py
python materias/metodologia-sistemas-ii/unidad-2-patrones-diseno/tp3-observer/inventory_observer_Nicolas_Viruel.py
```

## Regenerar PDFs

```powershell
cd materias/metodologia-sistemas-ii/unidad-2-patrones-diseno
python build_pdf.py tp1-factory-method/tp1-resuelto_Nicolas_Viruel.md
python build_pdf.py tp2-adapter/tp2-resuelto_Nicolas_Viruel.md
python build_pdf.py tp3-observer/tp3-resuelto_Nicolas_Viruel.md
```

## Estado

| Ítem | Estado |
|------|--------|
| Consignas descargadas | ✅ |
| TP1 Factory Method | ✅ Código + PDF |
| TP2 Adapter | ✅ Código + PDF |
| TP3 Observer | ✅ Código + PDF |
| Subida a Moodle | ⏳ Subir los 3 PDF listos abajo |
