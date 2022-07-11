from plyer import filechooser
path = filechooser.open_file(title="Pick a CSV file..", 
                             filters=[("Documents", "*.docx")])