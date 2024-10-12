from groq import Groq
import shutil
import os
from typing import Final
from docx import Document
from .coverletter import fill_invatiation

TOKEN = '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'

client1 = Groq(
    api_key=TOKEN
)

def export(resume, jobdescription):
    resume_text = resume
    job_text = jobdescription
    prompt = "With this job description here       "+job_text+"create a coverletter for a student looking for an internship tailoring it to my resume here      "+resume_text+" This will be only one paragraph, You do not need to include dear hiring manager, you do not need to include Here is the cover letter below: . The first sentence will be about what position i am applying for. The second sentence will talk about my education at the university and my major with deep interest in what skills that the job description requires me to have. the next sentences will talk about why I am qualified for this job and should include key words from the job description. Please do not include this the fact that you have created it, it is not needed. MAKE SURE TO START YOUR RESPONSE WITH  As a current student....    Make this prompt at most 100 words.   "
    response1 = client1.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
            {"role":"user", "content": prompt}
                    
                    
                    
                    
            ]
        )
    generatedtext = str(response1.choices[0].message.content.strip())
    return generatedtext