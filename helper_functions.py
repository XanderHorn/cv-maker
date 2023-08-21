from jinja2 import Template
import pandas as pd
import numpy as np

def render_cv(data, template):
    t = Template(template)
    return t.render(data)

def render_html_file(html_content, file_path):
    with open(file_path, "w") as f:
        f.write(html_content)
    f.close()

def create_template_from_excel():

    df = pd.read_excel('data/cv-input.xlsx', sheet_name = None, dtype='str')

    init_df = df['Configuration']
    init_df['Value'] = np.where(init_df['Value'].isnull(), None, init_df['Value'])
    init_df = init_df.set_index('Key')
    data = init_df.to_dict()['Value']

    data['overview'] = df['Overview']['Overview'].str.replace('\n', '<br>').item()
    data['jobs']= []
    data['education']= []
    data['languages']= []
    data['skills'] = []

    for sheet_name, tmp_df in df.items():
        if sheet_name == 'Skills':
            data["skills"] = tmp_df['Skills'].dropna().tolist()
        elif sheet_name == 'Experience':
            for _, row in tmp_df.iterrows():
                job = {
                    "role": row["Role"],
                    "company": row["Company"],
                    "duration": f"{row['From date']} to {row['To date']}",
                    "location": row["Location"],
                    "description": '<br>' + row["Description"].replace('\n', '<br>')
                }
                data["jobs"].append(job)
        elif sheet_name == 'Education':
            for _, row in tmp_df.iterrows():
                education = {
                    "institution": row["Insitution"],
                    "degree": row["Degree"],
                    "duration": f"{row['From date']} to {row['To date']}",
                    "description": '<br>' + row["Description"].replace('\n', '<br>')
                }
                data["education"].append(education)
        elif sheet_name == 'Languages':
            data["languages"] = tmp_df['Language'].dropna().tolist()
    return data