import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from pylatex import Document, Section, Command, NoEscape
from pylatex.utils import bold

# Función para generar el informe LaTeX
def generate_latex_report(data):
    doc = Document()
    doc.preamble.append(Command('title', data['Titulo']))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    # Portada
    with doc.create(Section(data['Portada'], numbering=False)):
        doc.append("Autor: ")
        doc.append(data['Autor'])
        doc.append(NoEscape(r'\\ '))  # Agregar espacio y salto de línea
        doc.append("Fecha: ")
        doc.append(data['Fecha'])
        doc.append(NoEscape(r'\\ '))  # Agregar espacio y salto de línea
        doc.append("Empresa: ")
        doc.append(data['Empresa'])
        doc.append(NoEscape(r'\\ '))  # Agregar espacio y salto de línea

    # Generar el índice
    with doc.create(Section("Índice", numbering=False)):
        sections_with_content = {}  # Para rastrear las secciones con contenido y su orden
        order = 1
        for section_name, section_content in data['Secciones'].items():
            if section_content.strip():
                sections_with_content[section_name] = order  # Registrar la página
                doc.append(section_name)
                doc.append(NoEscape(r'\dotfill'))  # Separador
                if section_name == "Objetivos específicos":
                    doc.append(str(order - 1))  # Mismo número de página para "Objetivo General" y "Objetivos específicos
                else:
                    doc.append(str(order))  # Número de página
                doc.append(NoEscape(r'\newline'))  # Nueva línea
                order += 1

    def add_section(section_name, section_title):
        section_content = data['Secciones'][section_name]
        if section_content.strip():
            doc.append(NoEscape(r'\newpage'))  # Agregar nueva página
            with doc.create(Section(section_title, numbering=False)):
                doc.append(section_content)

    # Sección "Planteamiento problema"
    add_section("Planteamiento problema", "Planteamiento problema")

    # Sección "Introducción"
    add_section("Introducción", "Introducción")

    # Sección "Resúmen"
    add_section("Resúmen", "Resúmen")

    # Sección "Limitaciones"
    add_section("Limitaciones", "Limitaciones")

    # Sección "Alcance"
    add_section("Alcance", "Alcance")

    # Sección "Objetivo General"
    objetivos_content = data['Secciones']["Objetivo General"]
    if objetivos_content.strip():
        doc.append(NoEscape(r'\newpage'))  # Agregar nueva página
        with doc.create(Section("Objetivo General", numbering=False)):
            doc.append(objetivos_content)

    # Sección "Objetivos específicos"
    objetivos_especificos = data['Secciones']["Objetivos específicos"]
    if objetivos_especificos.strip():
        doc.append(NoEscape(r'\subsection*{Objetivos Específicos}'))
        doc.append(objetivos_especificos)

    # Sección "Justificación"
    add_section("Justificación", "Justificación")

    # Sección "Conclusión"
    add_section("Conclusión", "Conclusión")

    # Sección "Recomendaciones"
    recomendaciones = data['Secciones']["Recomendaciones"]
    if recomendaciones.strip():
        doc.append(NoEscape(r'\newpage'))  # Agregar nueva página
        with doc.create(Section("Recomendaciones", numbering=False)):
            doc.append(recomendaciones)

    # Sección "Bibliografía"
    bibliografia = data['Bibliografia']
    if bibliografia.strip():
        doc.append(NoEscape(r'\newpage'))  # Agregar nueva página
        with doc.create(Section("Bibliografía", numbering=False)):
            doc.append(bibliografia)

    doc.generate_pdf('informe_profesional', clean_tex=True)

# Función para guardar el informe LaTeX y generar el PDF
def save_and_generate_report():
    data = {
        "Titulo": titulo_entry.get(),
        "Portada": portada_entry.get(),
        "Autor": autor_entry.get(),
        "Fecha": fecha_entry.get(),
        "Empresa": empresa_entry.get(),
        "Secciones": {},
        "Bibliografia": bibliografia_text.get(1.0, tk.END)
    }

    # Recopilar información de las secciones personalizadas
    for section_name, section_entry in secciones_entries.items():
        data['Secciones'][section_name] = section_entry.get(1.0, tk.END).strip()  # Eliminar espacios en blanco al inicio y al final

    # Generar el informe LaTeX
    generate_latex_report(data)
    messagebox.showinfo("Informe Generado", "El informe se ha generado con éxito.")

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Generador de Informes Profesionales")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Dividir la interfaz en cuatro columnas
left_column = tk.Frame(frame)
left_column.pack(side=tk.LEFT, padx=10)
right_column = tk.Frame(frame)
right_column.pack(side=tk.LEFT, padx=10)
right_column2 = tk.Frame(frame)
right_column2.pack(side=tk.LEFT, padx=10)
right_column3 = tk.Frame(frame)
right_column3.pack(side=tk.LEFT, padx=10)

# Campos en la primera columna
titulo_label = tk.Label(left_column, text="Título del Informe:")
titulo_label.pack()
titulo_entry = tk.Entry(left_column)
titulo_entry.pack()

portada_label = tk.Label(left_column, text="Nombre de la Portada:")
portada_label.pack()
portada_entry = tk.Entry(left_column)
portada_entry.pack()

autor_label = tk.Label(left_column, text="Nombre del Autor:")
autor_label.pack()
autor_entry = tk.Entry(left_column)
autor_entry.pack()

fecha_label = tk.Label(left_column, text="Fecha de Realización:")
fecha_label.pack()
fecha_entry = tk.Entry(left_column)
fecha_entry.pack()

empresa_label = tk.Label(left_column, text="Empresa o Institución:")
empresa_label.pack()
empresa_entry = tk.Entry(left_column)
empresa_entry.pack()

# Secciones personalizadas en las siguientes tres columnas
secciones_entries = {}

secciones_label = tk.Label(right_column, text="Secciones Personalizadas:")
secciones_label.pack()

secciones_nombres = [
    "Planteamiento problema",
    "Introducción",
    "Resúmen",
    "Limitaciones"
]

for nombre in secciones_nombres:
    label = tk.Label(right_column, text=nombre)
    label.pack()
    entry = tk.Text(right_column, height=6, width=40)
    entry.pack()
    secciones_entries[nombre] = entry

secciones_label2 = tk.Label(right_column2, text="Secciones Personalizadas:")
secciones_label2.pack()

secciones_nombres2 = [
    "Alcance",
    "Objetivo General",
    "Objetivos específicos",
    "Justificación"
]

for nombre in secciones_nombres2:
    label = tk.Label(right_column2, text=nombre)
    label.pack()
    entry = tk.Text(right_column2, height=6, width=40)
    entry.pack()
    secciones_entries[nombre] = entry

secciones_label3 = tk.Label(right_column3, text="Secciones Personalizadas:")
secciones_label3.pack()

secciones_nombres3 = [
    "Conclusión",
    "Recomendaciones"
]

for nombre in secciones_nombres3:
    label = tk.Label(right_column3, text=nombre)
    label.pack()
    entry = tk.Text(right_column3, height=6, width=40)
    entry.pack()
    secciones_entries[nombre] = entry

# Campos de bibliografía en la tercera columna
bibliografia_label = tk.Label(right_column3, text="Bibliografía:")
bibliografia_label.pack()
bibliografia_text = tk.Text(right_column3, height=6, width=40)
bibliografia_text.pack()

# Botón para generar el informe
generar_button = tk.Button(frame, text="Generar Informe", command=save_and_generate_report)
generar_button.pack()

root.mainloop()
