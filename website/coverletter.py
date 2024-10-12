import docx
from docx import Document
import os




def fill_invatiation(date,cn,loc,city,job,para):
    data = {
        '[Date]': date,
        '[Company Name]': cn,
        '[Location]': loc,
        '[City]': city,
        '[Job Title]': job,
        '[Paragraph]': para,

    } 
    doc = Document('output.docx')

    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if key in paragraph.text:
                for run in paragraph.runs:
                    run.text = run.text.replace(key,value)

    
    doc.save('website\output2.docx')
    return 0 
    



