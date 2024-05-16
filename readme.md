# Virtual Enviroment
* python -m venv env (creacion del enviroment llamado env) 
* env/Scripts/activate.bat (para activar el enviroment)
* otra forma es ir navegando cd env, cd Scripts y luego ejecutar activate.bat desde el cmd

# requirements.txt
* pip install -r requirements.txt (para instalar las dependencias necesarias del proyecto)   
  pip install pyinstaller (para generar el instalador)
* pyinstaller --onefile faena.py (para crear el ejecutable) (pip install pyinstaller)

# Modo de ejecucion
Debe existir un archivo llamado entrada.csv en el directorio 
Se debe ejecutar ingresos.exe en el mismo directorio del archivo entrada.csv
Se va a crear 1 directorio llamado /paraAnalisis donde se va guardar el archivo procesado
Se va a crear 1 directorio llamado /paraBackup donde se va guardar una copia del archivo entrada.csv
Se va a crear 1 archivo 1-estadisticas.pdf (si tiene letras rojas hay que prestar atencion a los datos)
Se va a crear 1 archivo 2-formatos.pdf (si tiene letras rojas hay que prestar atencion a los datos)
Se va a crear 1 archivo 3-cant_filas_y_nombre_columnas.pdf (si tiene letras rojas hay que prestar atencion a los datos)
Observaciones
Si se va a generar un archivo executable se debe cambiar el archivo funciones_archivos.py debido a los directorios temporales donde se almacenan en memoria