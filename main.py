from helper_functions import *
import pdfkit

template = open("data/cv-template.html", "r").read()

data = create_template_from_excel()

cv = render_cv(data, template)
render_html_file(cv, 'output/cv.html')
pdfkit.from_string(cv, 'output/cv.pdf', toc=False)