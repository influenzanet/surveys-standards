from jinja2 import Template, FileSystemLoader, Environment
from .survey import Question, MatrixDimensionList
import os
import datetime

def all_keys(d1, d2):
    d = list(d1.keys())
    for k in d2.keys():
        if k not in d:
            d.append(k)
    return d

def attr(o, name):
    if o is None:
        return '<>'
    if hasattr(o, name):
        return getattr(o, name)
    else:
        return '<None>'

def all_attributes(d1, d2, name):
    
    dd = []
    #show = isinstance(d1, MatrixDimensionList)
    #if show:
    #    print('start-----')
    #    print(d1)
    if d1 is not None:
        for d in d1.values():
            v = getattr(d, name, None)
    #        if show:
    #            print("d1----")
    #            print(d)
    #            print(v)
            if v is not None:
                dd.append(v)
    #if show:
    #    print(dd)
    if d2 is not None:
        for d in d2.values():
            v = getattr(d, name, None)
    #       if show:
    #            print("d2----")
    #            print(d)
    #            print(v)
            if v not in dd and v is not None:
                dd.append(v)
    #if show:
    #    print(dd)
    #    print('----ends')
    return dd


def create_empty_question():
    q = Question(None, 'none', '<Empty>')
    return q


def compare_legacy_to_html(survey, legacy, survey_name, legacy_name):
    """
    Compare 2 surveys models
    """
    path = os.path.dirname(os.path.abspath(__file__)) +  '/../templates/'

    env = Environment(
      loader=FileSystemLoader(path),
        autoescape='html',
    )

    env.globals['all_keys'] = all_keys
    env.globals['attr'] = attr
    env.globals['all_attributes'] = all_attributes

    template = env.get_template('legacy.html')
    
    with open(path + 'survey.css') as f:
        theme = f.read()

    ctx = {
        'survey_name': survey_name, 
        'legacy_name': legacy_name,
        'empty_question': create_empty_question(),
        'legacy': legacy,
        'survey': survey,
        'theme_css': theme
    }
    return template.render(ctx)

def survey_to_html(survey, version):
    """
    Create survey document
    """
    path = os.path.dirname(os.path.abspath(__file__)) +  '/../templates/'

    env = Environment(
      loader=FileSystemLoader(path),
        autoescape='html',
    )

    env.globals['all_keys'] = all_keys
    env.globals['attr'] = attr
    env.globals['all_attributes'] = all_attributes

    template = env.get_template('survey.html')
    
    with open(path + 'survey.css') as f:
        theme = f.read()

    ctx = {
        'build_date': datetime.datetime.now(),
        'version': version,
        'survey': survey,
        'theme_css': theme
    }
    return template.render(ctx)