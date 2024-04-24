
from django.shortcuts import render, redirect
from .models import PDF
import PyPDF2
import re
import io

def import_success(request):
    return render(request, 'import_success.html')

def eliminar_cabecera(texto):
    patron_eliminar = r'C[ ]?a[ ]?r[ ]?r[ ]?e[ ]?r[ ]?a\s+d[ ]?e\sI[ ]?n[ ]?g[ ]?e[ ]?n[ ]?i[ ]?e[ ]?r[ ]?í[ ]?a\s+(?:e[ ]?n\s+)?(?:C[ ]?i[ ]?v[ ]?i[ ]?l|E[ ]?l[ ]?é[ ]?c[ ]?t[ ]?r[ ]?i[ ]?c[ ]?a|E[ ]?l[ ]?e[ ]?c[ ]?t[ ]?r[ ]?ó[ ]?n[ ]?i[ ]?c[ ]?a|I[ ]?n[ ]?f[ ]?o[ ]?r[ ]?m[ ]?á[ ]?t[ ]?i[ ]?c[ ]?a)\s+F[ ]?a[ ]?c[ ]?u[ ]?l[ ]?t[ ]?a[ ]?d\s+d[ ]?e\s+C[ ]?i[ ]?e[ ]?n[ ]?c[ ]?i[ ]?a[ ]?s\s+y\s+T[ ]?e[ ]?c[ ]?n[ ]?o[ ]?l[ ]?o[ ]?g[ ]?í[ ]?a[ ]?s'
    texto_sin_cabecera = re.sub(patron_eliminar, "", texto)
    return texto_sin_cabecera

def importar_pdf(request):
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        pdf_files = request.FILES.getlist('pdf_files')

        for pdf_file in pdf_files:
            # Leer el contenido del archivo PDF
            file_content = pdf_file.read()

            # Crear un objeto PdfReader con el contenido del archivo
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))

            text = ""
            
            # Iterar sobre todas las páginas del PDF
            for no_page in range(len(pdf_reader.pages)):
                info_page = pdf_reader.pages[no_page]
                texto_pagina = info_page.extract_text()
                texto_sincab = eliminar_cabecera(texto_pagina)
                text += texto_sincab

            print(text)
            nombre_archivo = pdf_file.name
            materia = None
            codigo = None
            condicion = None
            curso = None
            semestre = None
            requisitos = None
            carga_horaria_semanal = None
            carga_horaria_semestral = None
            carrera = None
            fundamentacion = None
            objetivos_text = None
            contenido = None
            metodologia = None
            evaluacion = None
            bibliografia = None

            # Extraer datos del PDF
            materia_match = re.search(
                r'Nombre\s*de\s*la\s*Materia\s*:\s*(.*)', text)
            materia = materia_match.group(1).strip() if materia_match else None
            materia = re.sub(r'\.\s*$', '', materia) if materia else None

            codigo_match = re.search(r'Código\s*:\s*(.*)', text)
            codigo = codigo_match.group(1).strip().replace(
                " ", "") if codigo_match else None
            codigo = re.sub(r'\.\s*$', '', codigo) if codigo else None

            condicion_match = re.search(r'Condición\s*:\s*(.*)', text)
            condicion = condicion_match.group(1).strip().replace(
                " ", "") if condicion_match else None
            condicion = re.sub(r'\.\s*$', '', condicion) if condicion else None

            curso_match = re.search(r'Curso\s*:\s*(.*)', text)
            curso = curso_match.group(1).strip().replace(
                " ", "") if curso_match else None
            curso = re.sub(r'\.\s*$', '', curso) if curso else None

            semestre_match = re.search(r'Semestre\s*:\s*(.*)', text)
            semestre = semestre_match.group(1).strip().replace(
                " ", "") if semestre_match else None
            semestre = re.sub(r'\.\s*$', '', semestre) if semestre else None

            requisitos_match = re.search(r'Requisitos\s*:\s*(.*)', text)
            requisitos = requisitos_match.group(
                1).strip() if requisitos_match else None
            requisitos = re.sub(
                r'\.\s*$', '', requisitos) if requisitos else None

            carga_horaria_semanal_match = re.search(
                r'Carga\s+horaria\s+semanal\s*:\s*(.*)', text, re.IGNORECASE)
            carga_horaria_semanal = carga_horaria_semanal_match.group(
                1).strip() if carga_horaria_semanal_match else None
            carga_horaria_semanal = re.sub(
                r'\.\s*$', '', carga_horaria_semanal) if carga_horaria_semanal else None
            
            if 'Carga horaria' in text and carga_horaria_semanal is None:
                carga_horaria_semanal_match = re.search(
                    r'Carga\s+horaria\s*:\s*(.*)', text, re.IGNORECASE)
                carga_horaria_semanal = carga_horaria_semanal_match.group(
                    1).strip() if carga_horaria_semanal_match else None
                carga_horaria_semanal = re.sub(
                    r'\.\s*$', '', carga_horaria_semanal) if carga_horaria_semanal else None
            

            carga_horaria_semestral_match = re.search(
                r'Carga\s+horaria\s+semestral\s*:\s*(.*)', text, re.IGNORECASE)
            carga_horaria_semestral = carga_horaria_semestral_match.group(
                1).strip() if carga_horaria_semestral_match else None
            carga_horaria_semestral = re.sub(
                r'\.\s*$', '', carga_horaria_semestral) if carga_horaria_semestral else None
    
            
            if 'Total' in text and carga_horaria_semestral is None:
                carga_horaria_semestral_match = re.search(
                r'Total\s*:\s*(.*)', text, re.IGNORECASE)
            carga_horaria_semestral = carga_horaria_semestral_match.group(
                1).strip() if carga_horaria_semestral_match else None
            carga_horaria_semestral = re.sub(
                r'\.\s*$', '', carga_horaria_semestral) if carga_horaria_semestral else None
                

            carrera_match = re.search(r'Carrera\s*:\s*(.*)', text)
            carrera = carrera_match.group(1).strip() if carrera_match else None
            carrera = re.sub(r'\.\s*$', '', carrera) if carrera else None

            
            fundamentacion_match = re.search(
                r'FUNDAMENTAC[IÍÌÏ]ÓN\s*(?:\. )?(.*?)(?=III\.|IV\.|$)', text, re.DOTALL | re.IGNORECASE)
            fundamentacion = fundamentacion_match.group(
                1).strip() if fundamentacion_match else None

            objetivos_match = re.search(r'OBJETIVOS\s*(?:\. )?(.*?)(?=IV.|$)', text, re.DOTALL)
            objetivos_text = objetivos_match.group(1).strip() if objetivos_match else None

            if objetivos_text is None: 
                if 'CAPACIDADES GENERALES' in text:
                    capacidades_match = re.search(r'CAPACIDADES GENERALES\s*:\s*(.*)', text, re.IGNORECASE)
                    objetivos_text = capacidades_match.group(1).strip() if capacidades_match else None
                    objetivos_text = re.sub(r'\.\s*$', '', objetivos_text) if objetivos_text else None

            contenido_match = re.search(
                r'CONTENIDO\s*(?:\. )?(.*?)(?=V. |$)', text, re.DOTALL)
            contenido = contenido_match.group(
                1).strip() if contenido_match else None
            

            patron_metodologia = r'(?:V.\.|VI.\.)\s*METODOLOG(?:Í[ ]?A|[III])[ ]?A\s*(?:\. )?(.*?)(?=VI\.|VI-|VII\.|$)'
            metodologia_match = re.search(patron_metodologia, text, re.DOTALL)
            metodologia = metodologia_match.group(1).strip() if metodologia_match and metodologia_match.group(1) else None

                # si metodologia es None, intenta con el segundo patrón
            if metodologia is None:
             patron_metodologia = r'(?:V\.|VI\.)\s*ESTRATEGIAS\s+DE\s+EN[ ]?SEÑANZA[ ]?-APRENDIZAJE\s*(?:\. )?(.*?)(?=\s*(VI\.|VI-|VII\.)|$)'
             metodologia_match = re.search(patron_metodologia, text, re.DOTALL)
             metodologia = metodologia_match.group(1).strip() if metodologia_match and metodologia_match.group(1) else None
            

            evaluacion_match = re.search(
                r'EVALUACIÓN\s*(?:\. )?(.*?)(?=BIBLIOGRAFÍA|VII\.|\Z)', text, re.DOTALL)
            evaluacion = evaluacion_match.group(
                1).strip() if evaluacion_match else None
  
            bibliografia_match = re.search(
                r'BIBL[ ]?IOGRAF[ ]?ÍA\s*(?:\. )?(.*?)(?=\Z)', text, re.DOTALL)
            bibliografia = bibliografia_match.group(
                1).strip() if bibliografia_match else None

            # Guardar en la base de datos
            pdf = PDF(nombre=nombre_archivo, materia=materia,
                      carrera=carrera, codigo=codigo, objetivos=objetivos_text,
                      fundamentacion=fundamentacion, contenido=contenido, metodologia=metodologia,
                      evaluacion=evaluacion, bibliografia=bibliografia, condicion=condicion,
                      curso=curso, semestre=semestre, requisitos=requisitos,
                      carga_horaria_semanal=carga_horaria_semanal, carga_horaria_semestral=carga_horaria_semestral)
            pdf.save()

        return redirect('import_success')
    return render(request, 'import_pdf.html')

# Esta función se encarga de filtrar y mostrar las materias según la carrera seleccionada por el usuario.
def filtrar_materias(request):
    materias = [] # Inicializa una lista vacía para las materias
    
    carreras = PDF.objects.values_list('carrera', flat=True).distinct() # Obtiene las carreras distintas de la base de datos
    
    carrera_seleccionada = None  # Inicializa la variable para la carrera seleccionada como None

    if request.method == 'POST': # Verifica si la solicitud es mediante POST
        
        carrera_seleccionada = request.POST.get('carrera')# Obtiene la carrera seleccionada del POST
        
        materias = PDF.objects.filter(codigo__icontains=carrera_seleccionada) # Filtra las materias por el código de la carrera

    # Renderiza la plantilla 'seleccionar_pdf.html' con los datos necesarios(proceso de generar y mostrar la salida visual)
    return render(request, 'seleccionar_pdf.html', {
        'carreras': carreras,
        'carrera_seleccionada': carrera_seleccionada,
        'materias': materias,
    })
# Esta función se encarga de mostrar los detalles de un PDF específico basado en su código.
def mostrar_pdf(request, codigo): 
    try:
        # Intenta obtener el PDF con el código proporcionado
        pdf = PDF.objects.get(codigo=codigo) 
    except PDF.DoesNotExist:
        # Si no encuentra el PDF, asigna None
        pdf = None

    # Renderiza la plantilla 'mostrar_pdf.html' con el PDF correspondiente
    return render(request, 'mostrar_pdf.html', {'pdf': pdf})

