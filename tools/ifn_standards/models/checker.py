
from .survey import Survey


class SurveyChecker:

    def __init__(self) -> None:
        self.known_quids = []
        self.problems = []

    def report(self, level, problem, context):
        self.problems.append({'level': level, 'problem': problem, 'context': context})

    def check(self, survey):
        for quid, question in survey.questions.items():
            if question.data_name in self.known_quids:
                self.report('error', 'duplicate_data_name', {'value': question.data_name})
            else:
                self.known_quids.append(question.data_name)
            if question.has_response():
                known_values = []
                removed_values = []
                known_labels = []
                for r_name, response in question.responses.items():
                    if not response.active:
                        # Do not "check" inactive response, but check if code has been reaffected
                        removed_values.append(response.value)
                        continue
                    if response.value in known_values:
                        self.report('error', 'duplicate_response_value', {'question': question.data_name, 'value': response.value})
                    else:
                        known_values.append(response.value)
                    if response.value in removed_values:
                        self.report('warning', 'reassigned_value', {'question': question.data_name, 'value': response.value})
                    if response.text in known_labels:
                        self.report('error', 'duplicate_response_text', {'question': question.data_name, 'value': response.value})
                    else:
                        known_labels.append(response.text)
                    

    def show(self):
        """
            Print results
        """
        for p in self.problems:
            print("[%s] %s  %s"% (p['level'], p['problem'], str(p['context'])))
