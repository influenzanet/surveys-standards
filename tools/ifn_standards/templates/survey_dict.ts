
{% macro render_responses(responses) %}
 {%- for r in responses.values() %}
    '{{r.key}}': '{{r.value}}',
 {%- endfor %}
{% endmacro %}

const Survey{{name}} = {
{%- for quid in survey.questions -%}
{%- set question = survey.questions[quid] -%}
{%- if question.responses %}
    '{{quid}}': {
        {{- render_responses(question.responses) -}}
    },
{%- endif -%}
{%- endfor -%}
};