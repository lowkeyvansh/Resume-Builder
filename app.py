from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from fpdf import FPDF
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class ResumeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    summary = TextAreaField('Professional Summary', validators=[DataRequired()])
    experience = TextAreaField('Work Experience', validators=[DataRequired()])
    education = TextAreaField('Education', validators=[DataRequired()])
    skills = TextAreaField('Skills', validators=[DataRequired()])
    submit = SubmitField('Generate Resume')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resume', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_section(self, title, body):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ResumeForm()
    if form.validate_on_submit():
        pdf = PDF()
        pdf.add_page()
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, form.name.data, 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Email: {form.email.data}', 0, 1, 'C')
        pdf.cell(0, 10, f'Phone: {form.phone.data}', 0, 1, 'C')
        
        pdf.add_section('Professional Summary', form.summary.data)
        pdf.add_section('Work Experience', form.experience.data)
        pdf.add_section('Education', form.education.data)
        pdf.add_section('Skills', form.skills.data)

        pdf_file = f'resumes/{form.name.data.replace(" ", "_")}.pdf'
        pdf.output(pdf_file)

        return send_file(pdf_file, as_attachment=True)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    if not os.path.exists('resumes'):
        os.makedirs('resumes')
    app.run(debug=True)
