from typing import Deque
from cliff.command import Command
from . import register
import jsonschema
from ..utils import read_json, to_json
import sys
import os
from ..models import json_parser_survey, xml_parser_survey, compare_legacy_to_html, survey_to_html, survey_to_dict
from ..models.checker import SurveyChecker
import xml.etree.ElementTree as ET

class Output:

    def __init__(self, file):
        if file is not None:
            need_close = True
            self.out = open(file, 'w')
        else:
            need_close = False
            self.out = sys.stdout
        self.need_close = need_close

    def write(self, contents):
        self.out.write(contents)
    
    def close(self):
        if self.need_close:
            self.out.close()

def to_path(path: Deque):
    v = []
    for p in path:
        v.append(str(p))
    return "/".join(v)

class Validate(Command):
    """
        Validate survey description file agaisnt json schema 
    """

    name = 'survey:validate'

    def get_parser(self, prog_name):
        parser = super(Validate, self).get_parser(prog_name)
        parser.add_argument("file", help="Survey description file", action="store")
        return parser

    def take_action(self, args):
        json = read_json(args.file)

        p = self.app.get_schemas_path()
        
        schema = read_json(p + '/survey-description/v1.json')
       
        try:
            jsonschema.validate(json, schema)
            print("Json schema %s is valid" % (args.file))
        except jsonschema.ValidationError as e:
            path = e.absolute_path
            print("Error during validation at", to_path(path))
            print(e.message)
            print("Schema path ", to_path(e.schema_path))
            if(path[0] == "questions"):
                quid = path[1]
                q = json['questions'][quid]
                print("Question : %s %s" % (str(quid), q['data_name']))
                if len(path) > 3 and path[2] == "possible_responses":
                    rid = path[3]
                    r = q['possible_responses'][rid]
                    print("  Response #%s [%s]" % (str(rid), r['value']) )


class Show(Command):
    """
        Show survey description file agaisnt json schema 
    """

    name = 'survey:show'

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument("file", help="Survey file", action="store")
        parser.add_argument("--tag", help="Version to show about the survey", required=False, action="store")
        parser.add_argument("--template", help="Template to use", required=False, action="store")
        parser.add_argument("--output", help="path of file to output results", required=False)
        return parser

    def take_action(self, args):
        json = read_json(args.file)

        out = Output(args.output)
        
        survey = json_parser_survey(json)

        opts = {}
        if args.template:
            opts['template'] = args.template

        output = survey_to_html(survey, version=args.tag, opts=opts)
        out.write(output)
        out.close()

class Legacy(Command):
    """
        Compare with legacy xml 
    """

    name = 'survey:legacy'

    def get_parser(self, prog_name):
        parser = super(Legacy, self).get_parser(prog_name)
        parser.add_argument("file", help="Survey file", action="store")
        parser.add_argument("xml", help="Survey file xml", action="store")
        parser.add_argument("--output", help="path of file to output results", required=False)
        return parser

    def take_action(self, args):
        json = read_json(args.file)
        survey = json_parser_survey(json)

        tree = ET.parse(args.xml)
        legacy = xml_parser_survey(tree)

        out = Output(args.output)
        
        output = compare_legacy_to_html(survey=survey, legacy=legacy, survey_name=os.path.basename(args.file), legacy_name=os.path.basename(args.xml) )
        out.write(output)

        out.close()

class Transform(Command):
    """
        Validate survey description file agaisnt json schema 
    """

    name = 'survey:transform'

    def get_parser(self, prog_name):
        parser = super(Transform, self).get_parser(prog_name)
        parser.add_argument("file", help="Survey file", action="store")
        return parser

    def take_action(self, args):
        json = read_json(args.file)

        for question in json['questions']:
            if 'possible_responses' in question:
                for r in question['possible_responses'].values():
                    if 'data_name' in r:
                        del r['data_name']
                    if 'description' in r:
                        if r['description'] != '':
                            r['comment'] = r['description']
                        del r['description']
            if 'description' in question:
                if question['description'] != '':
                    question['comment'] = question['description']
                del question['description']
        print(to_json(json))


class Dictionary(Command):
    """
        Validate survey description file agaisnt json schema 
    """

    name = 'survey:dictionary'

    def get_parser(self, prog_name):
        parser = super(Dictionary, self).get_parser(prog_name)
        parser.add_argument("--file", help="Survey file", action="store", required=False)
        parser.add_argument("name", help="Survey name", action="store")
        parser.add_argument("--output", help="path of file to output results", required=False)
        return parser

    def take_action(self, args):
        
        file = args.file
        name = args.name
        out = Output(args.output)

        if file is None:
            file="surveys/%s/survey.json" % (name, )
            print("Using survey in '%s'" % file)
            
        json = read_json(file)

        survey = json_parser_survey(json)
        
        output = to_json(survey_to_dict(survey, survey_name=name), indent=2)

        out.write(output)

        out.close()

class Checker(Command):
    """
        Check the survey consistency
    """

    name = 'survey:check'

    def get_parser(self, prog_name):
        parser = super(Checker, self).get_parser(prog_name)
        parser.add_argument("--file", help="Survey file", action="store", required=False)
        parser.add_argument("name", help="Survey name", action="store")
        parser.add_argument("--output", help="path of file to output results", required=False)
        return parser

    def take_action(self, args):
        
        file = args.file
        name = args.name
        out = Output(args.output)

        if file is None:
            file="surveys/%s/survey.json" % (name, )
            print("Using survey in '%s'" % file)
            
        json = read_json(file)

        survey = json_parser_survey(json)
        
        checker = SurveyChecker()
        checker.check(survey)

        if args.output:
            out.write(to_json(checker.problems, indent=2))
            out.close()
        else:
            checker.show()

register(Validate)
register(Show)
register(Legacy)
register(Transform)
register(Dictionary)
register(Checker)