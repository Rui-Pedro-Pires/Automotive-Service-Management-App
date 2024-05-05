import mysql.connector
from serviços_list import tipo_serviço

conn = mysql.connector.connect(
  host="sql8.freesqldatabase.com",
  user="sql8704076",
  password="DWIEWlMnpi",
  database="sql8704076"
)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS clientes")
conn.commit()

cursor.execute("""CREATE TABLE clientes (
               id INT AUTO_INCREMENT PRIMARY KEY,
               data_marcação VARCHAR(255),
               hora_marcação VARCHAR(255),
               data_entrega VARCHAR(255),
               hora_entrega VARCHAR(255),
               cliente VARCHAR(255),
               telemovel INT,
               email VARCHAR(255),
               matricula VARCHAR(255),
               marca VARCHAR(255),
               modelo VARCHAR(255),
               kmx INT,
               ano INT)
            """)
conn.commit()

cursor.execute("DROP TABLE IF EXISTS serviços")
conn.commit()

cursor.execute("CREATE TABLE serviços (ID INT AUTO_INCREMENT PRIMARY KEY, serviço VARCHAR(255))")
conn.commit()

for serviço in tipo_serviço:
    cursor.execute("INSERT INTO serviços (serviço) VALUES (%s)", (serviço,))
    conn.commit()

cursor.execute("DROP TABLE IF EXISTS cliente_serviços")
conn.commit()

cursor.execute("CREATE TABLE cliente_serviços (clienteID INT, serviço VARCHAR(255))")
conn.commit()

cursor.close()
conn.close()