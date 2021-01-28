from xml.etree import ElementTree
from collections import OrderedDict

class Survey:

    def __init__(self, name):
        self.name = name
        self.questions = OrderedDict()

    def add_question(self, question):
        n = question.data_name
        if n in self.questions:
            raise Exception("Question with data_name '%s' is already defined" % (n))
        self.questions[n] = question

class Question:
    
    def __init__(self, data_name, type, title):
        self.data_name = data_name
        self.data_type = None
        self.type = type
        self.mandatory = False
        self.title = title
        self.comment = None
        self.data_type = None
        self.responses = ResponseList()
        self.rows = MatrixDimensionList()
        self.columns = MatrixDimensionList()
        self.order = 0
        self.active = True
        self.plateforms = []
        self.target = None
    
    def add_response(self, response):
        self.responses[response.key] = response
    
    def set_rows(self, rows):
        self.rows = rows
    
    def set_columns(self, columns):
        self.columns = columns

class ResponseList(OrderedDict):

    def find_by(self, name, value):
        for k, r in self.items():
            if hasattr(r, name):
                if getattr(r, name) == value:
                    return r
        return None

class Response:
      """
        key: local key in the spec
        text: label of the response
        order: order in the spec
        value: 
      """
      
      def __init__(self, key, text, order):
          self.key = key
          self.text = text
          self.order = order
          self.value = None
          self.comment = None
          self.active = True
          self.extra = None
          self.added_at = None
          self.removed_at = None
          self.plateforms = []


class MatrixDimension:
    def __init__(self, text, key, value, order):
        """
            text: label
            key: key of the element in the definition (db id or json key dict)
            value: value to be used in the model
            order: order of the element in the definition
        """
        self.text = text
        self.key = key
        self.value = value
        self.order = order
        self.added_at = None
        self.removed_at = None

    def __repr__(self):
        return "[%s](%s)#%d" % (self.value, self.text, self.order)

class MatrixDimensionList(OrderedDict):
    
    def find_by(self, name, value):
        for k, r in self.items():
            if hasattr(r, name):
                if getattr(r, name) == value:
                    return r
        return None

def json_parser_survey(survey):
    """
        survey from json dictionnary
    """
    ss = Survey(survey['name'])
    index = 1
    for qDef in survey['questions']:
        q = json_parser_question(qDef)
        q.order = index
        ss.add_question(q)
        index = index + 1
    return ss

def json_parser_comment(json):
    if isinstance(json, str):
        return [json]
    return json

def json_parser_description(json):
    if isinstance(json, str):
        return [json]
    return json


def import_attr(obj, data, keys):
    for key in keys:
        if key in data:
            setattr(obj, key, data[key])

def json_parser_question(json):
    """
        question definition from json
    """
    data_name = json['data_name']

    q = Question(data_name, json['type'], json['title'])
    
    if 'description' in json:
        q.description = json_parser_description(json['description'])
    
    if 'mandatory' in json:
        q.mandatory = json['mandatory']
  
    if 'comment' in json:
        q.comment = json_parser_comment(json['comment'])

    import_attr(q, json, ['active','data_type', 'format','rules', 'added_at', 'removed_at', 'platforms', 'target'])

    if 'possible_responses' in json:
        index = 1
        for key, rDef in json['possible_responses'].items():
            try:
                r = json_parser_response(key, rDef, index)
            except Exception as e:
                raise Exception("Error in %s/%s : %s " % (data_name, key, e))
            q.add_response(r)
            index = index + 1

    if 'rows' in json:
        q.rows = json_parser_matrix_dim(json['rows'])

    if 'columns' in json:
        q.columns = json_parser_matrix_dim(json['columns'])

    return q

def json_parser_response(key, json, index):
    
    if not 'text' in json:
        raise Exception("Missing 'text' field")
    
    r = Response(key, json['text'], index)
    
    import_attr(r, json, ['added_at', 'removed_at', 'platforms'])

    if 'value' in json:
        r.value = json['value']
    
    if 'description' in json:
        r.description = json_parser_description(json['description'])
    
    if 'comment' in json:
        r.comment = json_parser_comment(json['comment'])

    return r

def json_parser_matrix_dim(json):
    rr = MatrixDimensionList()
    index = 1
    for key, d in json.items():
        #print(key, d)
        m = MatrixDimension(d['text'], key, d['value'], index)
        rr[key] = m
        index = index + 1
    return rr
    

def with_ns(n):
    return '{http://dndg.it/ns/pollster-1.0}' + n

def xml_parser_survey(tree):
    """
        Parse Survey from legacy Xml format (Pollster Influenzanet)

        xml: xml.etree.ElementTree
    """
    xml = tree.getroot()
    name = xml.find(with_ns('shortname')).text

    survey = Survey(name)

    xqq = xml.find(with_ns('questions'))
    index = 1
    for qx in xqq.iter(with_ns('question')):
        question = xml_parser_question(qx)
        question.order = 1
        survey.add_question(question)
        index = index + 1
    return survey

def xml_parser_question(xml):
    title = xml.find(with_ns('title')).text
    data_name = xml.find(with_ns('data_name')).text
    data_type = xml.find(with_ns('data_type')).text

    if data_type != '':
        data_type = data_type.replace('wok.pollster.datatypes.','')
    else:
        data_type = None

    qtype = xml.find(with_ns('type')).text
    mandatory = xml.find(with_ns('is_mandatory')).text
    description = xml.find(with_ns('description')).text

    question = Question(data_name, qtype, title)
    question.mandatory = mandatory == "true"
    question.description = description
    question.data_type = data_type

    options = xml.find(with_ns('options'))
   
    index = 1
    for o in options:
        r = xml_parser_option(o, index)
        if r is not None:
            question.add_response(r)
            index = index + 1

    rows = xml_parser_dim(xml.find(with_ns('rows')), 'row', 'row')
    columns = xml_parser_dim(xml.find(with_ns('columns')), 'column', 'col')
    
    question.rows = rows
    question.columns = columns
    return question
    

def xml_parser_option(xml, index):
    
    # Skip virtual options
    v = xml.find(with_ns('is_virtual'))
    if v is not None and v.text == "true":
        return None
    
    key = xml.attrib['id']
    data_name = xml.find(with_ns('data_name')).text
    
    xt =  xml.find(with_ns('text'))
    if xt is not None:
        text  = xt.text
    else:
        text = ""
    value = xml.find(with_ns('value')).text
    opened = xml.find(with_ns('is_open')).text == "true"
    shown = xml.find(with_ns('starts_hidden')).text == "true"
    
    r = Response(key, text, index)
    r.data_name = data_name
    r.value = value
    r.extra = opened
    return r       

def xml_parser_dim(xml, tag, key_prefix):
    """
      xml= rows or columns node
      tag name of the node
    """
    rr = MatrixDimensionList()
    index = 1  # Order is implicit, so we trick a key, by creating it from order
    for r in xml:
        title = r.find(with_ns('title')).text
        key = r.attrib['id']
        data_name = "%s%d" % (key_prefix, index)
        d = MatrixDimension(title, key, data_name, index)
        rr[key] = d
        index = index + 1
    return rr
