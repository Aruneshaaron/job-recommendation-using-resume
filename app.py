from flask import Flask, render_template, request, session, redirect, url_for, flash
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import spacy
import pandas as pd
import re
import spacy
from nltk.corpus import stopwords
from main import predict,suggest_roles
import sqlite3

app=Flask(__name__)
app.secret_key = 'jndjsahdjxasudhas-09vzx2223'
database = "new.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS register (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT, user_email TEXT, password TEXT
    )
''')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form['user_name']   
        user_email = request.form['user_email']
        password = request.form['password']
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO register (user_name, user_email, password) VALUES (?, ?, ?)",
                       (user_name, user_email, password))
        conn.commit()
        flash('Registration successful!', 'success')
        return render_template('index.html')

    return render_template('index.html')

u=[]
name=[]
email=[]
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        user_email = request.form['user_email']
        password = request.form['password']
        cursor.execute("SELECT * FROM register WHERE user_email=? AND password=?", (user_email, password))
        user = cursor.fetchone()
        if user:
            u.append(user_email)
            name.append(user[1])
            email.append(user[2])
            return render_template('upload.html',name=user[1],email=user[2])
        else:
            return "password mismatch"
    return render_template('register.html')

nlp = spacy.load('en_core_web_sm')
result = []
with open('linkedin skill',encoding='utf-8') as f:
    external_source = list(f)
    
for element in external_source:
    result.append(element.strip().lower())



def extract_skill_1(resume_text):
    nlp_text = nlp(resume_text)
    tokens = [token.text for token in nlp_text if not token.is_stop]
    skills = result
    skillset = []
    for i in tokens:
        if i.lower() in skills: 
            skillset.append(i)
    for i in nlp_text.noun_chunks:
        i = i.text.lower().strip()
        if i in skills:
            skillset.append(i)
    return [word.capitalize() for word in set([word.lower() for word in skillset])]



STOPWORDS = set(stopwords.words('english'))
EDUCATION = [
            'CSE','EEE.', 'ECE', 'IT',"MCA"]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]
    edu = {}
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education






def extract_marks(resume_text):
    nlp_text = nlp(resume_text)
    mark_patterns = [
        [{'POS': 'NUM'}, {'ORTH': '%'}],
        [{'LOWER': 'grade'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NUM'}],
        [{'LOWER': 'cgpa'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NUM'}],
        [{'LOWER': 'marks'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NUM'}],
        [{'LOWER': 'percentage'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NUM'}],
        [{'LOWER': 'percent'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'NUM'}],
        [{'POS': 'NUM'}, {'ORTH': '%'}]  
    ]
    matcher = spacy.matcher.Matcher(nlp.vocab)
    matcher.add('MARK_PATTERN', mark_patterns)
    matches = matcher(nlp_text)
    extracted_marks = []
    for match_id, start, end in matches:
        mark_span = nlp_text[start:end]
        extracted_marks.append(mark_span.text)
    return extracted_marks





def extract_skill(resume_text):
    nlp_text = nlp(resume_text)
    tokens = [token.text for token in nlp_text if not token.is_stop]
    skills = ['python', 'machine learning', 
               'css', 'C++', 'data science',
               'PHP', 'mySQL', 'HTML', 'SQL',
             'tensorflow', 'deep learning',
             'pandas', 'opencv', 'typescript', 'c#',
              'data factory', 'ci/cd']
    skillset = []
    for i in tokens:
        if i.lower() in skills:
            skillset.append(i)
    for i in nlp_text.noun_chunks:
        i = i.text.lower().strip()  
        if i in skills:
            skillset.append(i)
    return [word.capitalize() for word in set([word.lower() for word in skillset])]
@app.route('/back')
def back():
    return render_template('upload.html')
@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        i_f=request.files['resume_file']
        resMgr = PDFResourceManager()
        retData = io.StringIO()
        TxtConverter = TextConverter(resMgr,retData, laparams= LAParams())
        interpreter = PDFPageInterpreter(resMgr,TxtConverter)
        for page in PDFPage.get_pages(i_f):
            interpreter.process_page(page)
            txt = retData.getvalue()
            
        def extractResume(resume_text):
            skill = extract_skill(resume_text)
            skill_from_external = extract_skill_1(resume_text)
            mark=extract_marks(resume_text)
            degree = extract_education(resume_text)
            return skill,skill_from_external,mark,degree
        skill,skill1,mark,degree=extractResume(txt)
        totallskill=skill+skill1
        low=[]
        for i in totallskill:
            a=i.lower()
            low.append(a)


        percentages = []
        cgpa_values = []
        grades = []
        other_values = []

        for a in mark:
            item=a.lower()
            if '%' in item:
                percentage_value = float(item.strip('%')) / 10
                percentages.append(percentage_value)
            elif 'cgpa' in item:
                cgpa_value = ''.join(filter(str.isdigit, item))  
                cgpa_values.append(int(cgpa_value))
            elif 'grade' in item:
                 grade_value = float(''.join(filter(str.isdigit, item)))
                 
                 grades.append(grade_value)
            else:
                other_values.append(item)




                
        if len(cgpa_values)>0:
            l=max(cgpa_values)
        elif len(grades)>0:
            l=max(grades)
        elif len(percentages)>0:
            l=max(percentages)
        elif len(other_values)>0:
            l=max(other_values)
        else:
            return "could not find mark"
        value={' java':0,' javascript':1,' php':2,' python':3,' ruby':4,' sql':5, 'c':6,'css':7,'html':8,'bootstrap':9}
        skill=[]
        for i,j in value.items():
            if i in low:
                skill.append(j)


        if len(skill)>0:
            skill1=skill
        else:
            return "COULD NOT FIND  SKILL"
        final=[]
        for i in skill1:
            a=predict(l,i)
            
            for k in a:
                final.append(k)
            
        companies=set(final)

        c=[]
        for i in low:
            a=suggest_roles(i)
            c.append(a)
        job=set(c)
        return render_template('result.html', companies=companies, job=job)
   
    
if __name__=='__main__':
    app.run(port=800)




