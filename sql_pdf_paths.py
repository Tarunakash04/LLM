import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="RootUser@123",
)

if connection.is_connected():
    print("Connected to MySQL")

cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS pdf_database")
print("Database 'pdf_database' created successfully.")

cursor.execute("USE pdf_database")

create_table_query = """
CREATE TABLE IF NOT EXISTS pdf_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_path VARCHAR(255) NOT NULL
)
"""
cursor.execute(create_table_query)
print("Table 'pdf_files' created successfully.")

pdf_paths = [
    r"C:\Users\Tarun Akash\Downloads\2109.13916v5.pdf",
    r"C:\Users\Tarun Akash\Downloads\1-s2.0-S187705092202467X-main.pdf",
    r"C:\Users\Tarun Akash\Downloads\800055.802036.pdf",
    r"C:\Users\Tarun Akash\Downloads\king09a.pdf",
    r"C:\Users\Tarun Akash\Downloads\ECS-LFCS-86-2.pdf",
    r"C:\Users\Tarun Akash\Downloads\aaa.pdf",
    r"C:\Users\Tarun Akash\Downloads\1506.01066v2.pdf",
    r"C:\Users\Tarun Akash\Downloads\chee_wee_tan_et_al_natural_language_processing_acceptedversion.pdf",
    r"C:\Users\Tarun Akash\Downloads\jumping-nlp-curves.pdf",
    r"C:\Users\Tarun Akash\Downloads\evaluation.pdf"
]

for pdf_path in pdf_paths:
    insert_query = "INSERT INTO pdf_files (file_path) VALUES (%s)"
    cursor.execute(insert_query, (pdf_path,))
    connection.commit()
    print(f"PDF path '{pdf_path}' inserted successfully.")

cursor.close()
connection.close()

print("Connection closed.")
