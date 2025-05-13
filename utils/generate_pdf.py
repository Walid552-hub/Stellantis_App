from weasyprint import HTML
import os


def create_pdf(vin_data, output_dir="static/pdf"):
    generated_files = []

    for vin, tasks in vin_data.items():
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 30px;
                }}
                h1 {{
                    color: #003366;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                input[type=checkbox] {{
                    width: 20px;
                    height: 20px;
                }}
            </style>
        </head>
        <body>
            <h1>Rapport d'analyse - VIN : {vin}</h1>
            <p>Nombre de tâches : {len(tasks)}</p>
            <table>
                <thead>
                    <tr>
                        <th>Tâche</th>
                        <th>Etat de la tâche</th>
                    </tr>
                </thead>
                <tbody>
        """

        for task in sorted(set(tasks)):
            html_content += f"""
                <tr>
                    <td>{task}</td>
                    <td><input type="checkbox" disabled></td>
                </tr>
            """

        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """

        # Nom de fichier sécurisé
        pdf_filename = f"{vin}.pdf".replace("/", "_").replace(":", "_")
        output_path = os.path.join(output_dir, pdf_filename)

        HTML(string=html_content).write_pdf(output_path)
        generated_files.append(pdf_filename)

    return generated_files
