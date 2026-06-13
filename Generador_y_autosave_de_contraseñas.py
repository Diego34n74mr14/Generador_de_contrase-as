# Importamos las librerías necesarias del sistema y de Python
import sys
import os
import random
import string

# Importamos los componentes visuales específicos de la biblioteca PyQt5
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QCheckBox, QSpinBox, QTextEdit, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, QGroupBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Definimos la clase principal de nuestra aplicación que hereda de QWidget (una ventana)
class GeneradorContrasenas(QWidget):
    def __init__(self):
        super().__init__()
        
        # Obtenemos la ruta absoluta de la carpeta donde está guardado este script
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        
        # Creamos la ruta completa para el archivo TXT en esa misma carpeta
        self.archivo_datos = os.path.join(ruta_script, "mis_contrasenas.txt")
        
        # Construimos la interfaz gráfica llamando al método correspondiente
        self.initUI()

    def initUI(self):
        # Configuramos el título y el tamaño de la ventana
        self.setWindowTitle("Generador y Organizador de Contraseñas")
        self.resize(550, 600)
        self.setMinimumSize(500, 550) # Evita que se encoja demasiado

        # Aplicamos una tipografía legible para toda la interfaz
        fuente_global = QFont("Arial", 10)
        self.setFont(fuente_global)

        # Layout principal que ordenará todo de forma vertical (arriba a abajo)
        layout_principal = QVBoxLayout()

        # --- SECCIÓN: FORMULARIO DE DATOS ---
        grupo_registro = QGroupBox("Datos del Registro")
        layout_registro = QVBoxLayout()

        # Etiqueta y campo de texto para la plataforma
        layout_registro.addWidget(QLabel("Plataforma / Servicio:"))
        self.input_plataforma = QLineEdit()
        self.input_plataforma.setPlaceholderText("Ej: Google, Spotify, Banco...")
        layout_registro.addWidget(self.input_plataforma)

        # Etiqueta y campo de texto para el usuario
        layout_registro.addWidget(QLabel("Usuario / Correo Electrónico:"))
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ej: usuario@correo.com")
        layout_registro.addWidget(self.input_usuario)

        # Etiqueta para la contraseña
        layout_registro.addWidget(QLabel("Contraseña:"))
        
        # Sub-layout horizontal para poner la contraseña al lado del botón Copiar
        layout_password = QHBoxLayout()
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Escribe o genera una contraseña")
        layout_password.addWidget(self.input_password)
        
        # Botón para copiar el texto actual al portapapeles
        btn_copiar = QPushButton("Copiar")
        btn_copiar.setToolTip("Copiar contraseña al portapapeles")
        btn_copiar.clicked.connect(self.copiar_al_portapapeles)
        layout_password.addWidget(btn_copiar)
        
        # Añadimos el sub-layout horizontal al diseño del formulario
        layout_registro.addLayout(layout_password)

        # Asignamos el diseño al grupo de registro y lo añadimos a la vista principal
        grupo_registro.setLayout(layout_registro)
        layout_principal.addWidget(grupo_registro)

        # --- SECCIÓN: OPCIONES DEL GENERADOR ---
        grupo_generador = QGroupBox("Opciones del Generador Automático")
        layout_generador = QVBoxLayout()

        # Configuración para la longitud del texto
        layout_longitud = QHBoxLayout()
        layout_longitud.addWidget(QLabel("Longitud de la contraseña:"))
        self.spin_longitud = QSpinBox()
        self.spin_longitud.setRange(6, 32) # Mínimo 6, máximo 32 caracteres
        self.spin_longitud.setValue(12)  # 12 por defecto
        layout_longitud.addWidget(self.spin_longitud)
        layout_longitud.addStretch() 
        layout_generador.addLayout(layout_longitud)

        # Casillas de verificación para armar la mezcla de caracteres
        self.chk_mayus = QCheckBox("Incluir Mayúsculas (A-Z)")
        self.chk_mayus.setChecked(True)
        self.chk_minus = QCheckBox("Incluir Minúsculas (a-z)")
        self.chk_minus.setChecked(True)
        self.chk_numeros = QCheckBox("Incluir Números (0-9)")
        self.chk_numeros.setChecked(True)
        self.chk_simbolos = QCheckBox("Incluir Símbolos (!@#$%^&*)")
        self.chk_simbolos.setChecked(False)

        # Añadimos las casillas al diseño del generador
        layout_generador.addWidget(self.chk_mayus)
        layout_generador.addWidget(self.chk_minus)
        layout_generador.addWidget(self.chk_numeros)
        layout_generador.addWidget(self.chk_simbolos)

        # Botón con color personalizado para disparar el generador aleatorio
        btn_generar = QPushButton("⚡ Generar Contraseña Segura")
        btn_generar.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; padding: 6px;")
        btn_generar.clicked.connect(self.generar_contrasena)
        layout_generador.addWidget(btn_generar)

        # Asignamos el diseño al grupo del generador y lo sumamos a la vista principal
        grupo_generador.setLayout(layout_generador)
        layout_principal.addWidget(grupo_generador)

        # --- SECCIÓN: ACCIONES DE ALMACENAMIENTO ---
        layout_acciones = QHBoxLayout()
        
        # Botón para guardar datos
        btn_guardar = QPushButton("💾 Guardar Registro")
        btn_guardar.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 8px;")
        btn_guardar.clicked.connect(self.guardar_registro)
        layout_acciones.addWidget(btn_guardar)

        # Botón para eliminar el archivo TXT por completo
        btn_borrar_todo = QPushButton("🗑️ Borrar Todo el Historial")
        btn_borrar_todo.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; padding: 8px;")
        btn_borrar_todo.clicked.connect(self.borrar_historial)
        layout_acciones.addWidget(btn_borrar_todo)

        # Añadimos la fila de botones de acción al layout principal
        layout_principal.addLayout(layout_acciones)

        # --- SECCIÓN: VISOR EN TIEMPO REAL ---
        layout_principal.addWidget(QLabel("Tus Contraseñas Almacenadas:"))
        self.vista_registros = QTextEdit()
        self.vista_registros.setReadOnly(True) # Modo lectura para que no se altere manualmente
        layout_principal.addWidget(self.vista_registros)

        # Leemos el archivo TXT al arrancar para reflejar datos previos si los hay
        self.actualizar_vista_registros()
        
        # Establecemos el layout ordenado en la ventana
        self.setLayout(layout_principal)

    # --- FUNCIONES LÓGICAS ---

    def generar_contrasena(self):
        """Genera una cadena de caracteres aleatoria según las casillas marcadas."""
        caracteres_disponibles = ""
        
        if self.chk_minus.isChecked():
            caracteres_disponibles += string.ascii_lowercase
        if self.chk_mayus.isChecked():
            caracteres_disponibles += string.ascii_uppercase
        if self.chk_numeros.isChecked():
            caracteres_disponibles += string.digits
        if self.chk_simbolos.isChecked():
            caracteres_disponibles += "!@#$%^&*()-_=+"

        # Si el usuario desmarca todas las opciones, mostramos advertencia
        if not caracteres_disponibles:
            QMessageBox.warning(self, "Error de Opciones", "Debes activar al menos un tipo de carácter.")
            return

        # Construimos la contraseña seleccionando al azar la longitud deseada
        longitud = self.spin_longitud.value()
        password_generada = "".join(random.choice(caracteres_disponibles) for _ in range(longitud))
        self.input_password.setText(password_generada)

    def copiar_al_portapapeles(self):
        """Copia el texto del campo contraseña directamente al sistema."""
        texto = self.input_password.text()
        if texto:
            clipboard = QApplication.clipboard()
            clipboard.setText(texto)
            QMessageBox.information(self, "Copiado", "Contraseña copiada al portapapeles.")
        else:
            QMessageBox.warning(self, "Aviso", "No hay ningún texto en el campo de contraseña.")

    def guardar_registro(self):
        """Escribe un nuevo bloque de texto al final de nuestro archivo TXT."""
        plataforma = self.input_plataforma.text().strip()
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text().strip()

        # Validamos que los tres campos contengan información
        if not plataforma or not usuario or not password:
            QMessageBox.warning(self, "Campos Vacíos", "Completa la plataforma, usuario y contraseña antes de guardar.")
            return

        try:
            # Abrimos el archivo en modo 'a' (append) para añadir información al final
            with open(self.archivo_datos, "a", encoding="utf-8") as archivo:
                archivo.write(f"Plataforma: {plataforma}\n")
                archivo.write(f"Usuario:    {usuario}\n")
                archivo.write(f"Contraseña: {password}\n")
                archivo.write("-" * 40 + "\n") # Línea divisoria informativa

            QMessageBox.information(self, "Éxito", "Guardado de forma segura.")
            
            # Limpiamos los inputs para escribir el siguiente registro cómodamente
            self.input_plataforma.clear()
            self.input_usuario.clear()
            self.input_password.clear()
            
            # Volvemos a leer el archivo para mostrar la nueva contraseña abajo
            self.actualizar_vista_registros()
        except Exception as e:
            QMessageBox.critical(self, "Error de Guardado", f"No se pudo acceder al archivo:\n{str(e)}")

    def actualizar_vista_registros(self):
        """Carga el texto plano del archivo de texto en el cuadro visual de la pantalla."""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()
                if not contenido.strip():
                    self.vista_registros.setText("El archivo está vacío actualmente.")
                else:
                    self.vista_registros.setText(contenido)
            except Exception as e:
                self.vista_registros.setText(f"Error al leer la base de datos TXT:\n{str(e)}")
        else:
            self.vista_registros.setText("Historial limpio. No se ha generado ningún archivo de texto todavía.")

    def borrar_historial(self):
        """Borra físicamente el archivo .txt de la computadora tras una confirmación."""
        if not os.path.exists(self.archivo_datos):
            QMessageBox.information(self, "Aviso", "No existe un historial previo que eliminar.")
            return

        # Ventana emergente con opciones de SÍ o NO para evitar pérdidas por error
        respuesta = QMessageBox.question(self, "Confirmación Requerida", "¿Estás seguro de borrar permanentemente todas tus contraseñas?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if respuesta == QMessageBox.Yes:
            try:
                os.remove(self.archivo_datos)
                QMessageBox.information(self, "Eliminado", "El archivo TXT se ha borrado con éxito.")
                self.actualizar_vista_registros()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo borrar el archivo:\n{str(e)}")

# Bloque de inicio estándar para levantar y cerrar el proceso de PyQt5 de manera correcta
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeneradorContrasenas()
    ventana.show()
    sys.exit(app.exec_())