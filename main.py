from conection import conexion
import os
import datetime


# Create cursor
cursor = conexion.cursor()

# Name of db
nombre_db = "miasesordb2"

# Create dir for the back ups if it doesnt exit
backup_dir = "backups"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Create backup name
fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nombre_archivo_backup = f"{nombre_db}_backup_{fecha_actual}.sql"
ruta_archivo_backup = os.path.join(backup_dir, nombre_archivo_backup)

# Open backup file
with open(ruta_archivo_backup, 'w') as archivo:
    # Obtain tables structures
    cursor.execute("SHOW TABLES")
    for tabla in cursor.fetchall():
        tabla = tabla[0]
        cursor.execute(f"SHOW CREATE TABLE {tabla}")
        create_table_query = cursor.fetchone()[1]
        archivo.write(f"{create_table_query};\n\n")

        # Obtain and write the data in the file
        cursor.execute(f"SELECT * FROM {tabla}")
        for fila in cursor.fetchall():
            valores = ', '.join([f"'{str(valor)}'" for valor in fila])
            archivo.write(f"INSERT INTO {tabla} VALUES ({valores});\n")
        archivo.write("\n")


# Close cursor and connection
cursor.close()
conexion.close()

print("Backup completado exitosamente.")
