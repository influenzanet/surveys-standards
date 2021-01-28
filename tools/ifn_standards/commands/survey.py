from cliff.command import Command

from . import register
import jsonschema
from ..utils import read_json, to_json
import sys
import os
from ..models import json_parser_survey, xml_parser_survey, compare_legacy_to_html, survey_to_html

import xml.etree.ElementTree as ET

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
        
        print(p)

        schema = read_json(p + '/survey-description.json')
       
        jsonschema.validate(json, schema)
        print("Json schema is valid")

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

        need_close = True
        if args.output:
            need_close = True
            out = open(args.output, 'w')
        else:
            need_close = False
            out = sys.stdout

        survey = json_parser_survey(json)

        opts = {}
        if args.template:
            opts['template'] = args.template

        output = survey_to_html(survey, version=args.tag, opts=opts)
        out.write(output)

        if need_close:
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

        need_close = True
        if args.output:
            need_close = True
            out = open(args.output, 'w')
        else:
            need_close = False
            out = sys.stdout

        output = compare_legacy_to_html(survey=survey, legacy=legacy, survey_name=os.path.basename(args.file), legacy_name=os.path.basename(args.xml) )
        out.write(output)

        if need_close:
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
        

register(Validate)
register(Show)
register(Legacy)
register(Transform)