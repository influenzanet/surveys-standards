from simplejson import OrderedDict
from tools.ifn_standards.models.survey import Survey
import datetime

def survey_to_dict(survey: Survey, survey_name, opts={}):
    data = OrderedDict()
    data['_survey_'] = {
        "name": survey_name,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    for idx, question in survey.questions.items():
        if not question.has_response():
            continue
        quid = question.data_name
        rr = {}
        for name, resp in question.responses.items():
            rr[name] = resp.value
        data[quid] = rr
    return data

    
