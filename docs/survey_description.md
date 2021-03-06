# Survey Description Format

## Goals

The purpose of this format is to describe a survey and it's element in order to create documentation and facilitate survey maintenance and migration between legacy influenzanet platform and the new system. It's not as precise as a technical implementation for a survey engine (where a lot of technical details are specified).

## Structure

A survey is defined as a set of *Questions*.

### Question

*Question* is a the main element of a survey structure. One question contains textual fields to describe the expected data to be collected.

Common fields:
- **title**: Label of the question as to be presented to the user (after translation). 
- **type** : Kind of Question. Define how the data collection is organized
- **description** : Textual description of the question to the final user. Can be a string or an array of strings.
- **data_name**: name to be used to identify the question in the data
- **active** : can be used to indicate the question is inactive (value="false")            
- **comment** : Textual comments about the question for survey designer/scientific aspects. Can be a string or an array of strings.
- **mandatory**: is the field needs to be mandatory
- **added_at**: date when the question has been added
- **removed_at**: date when the question has been removed
- **data_type**: Can be used to describe the expected type of data to be collected from the data elements (numeric, text, date)
- **rules**: list of rules (textual description to be applied on this question). Array of strings.
- **platforms**: list of platforms (country code in upper case, e.g. 'UK') where the question is implemented if this item is specific.
- **target**: Target platforms, can be "all" (core question, expected every where) or "optional" (up to each platform to decide)
  
For type in 'text', 'date':
- **format** : for textual format describe how data of each data element must be entered (date, numeric, )

For type in 'single_choice', 'multiple_choice', 'matrix':
- **possible_responses** : list of possible responses, see Responses

For 'matrix' questions
- **rows**: list of rows
- **colums**: list of columns

#### Question types

- text: textual input (free text), with possible restriction/format
- single_choice: single response
- multiple_choice: several responses possible among a list of possibles
- matrix : rectangular

#### Rules

Rules are textual descriptions of conditions to apply to this questions (the runtime logic).

To facilitate reading and enable some check some syntax can be applied :

- '$name' refer to question with data_name "name"
- '[xxx]' refer to the label of a response 'xxx'
-  '#option_1' refer to the id of the item (response, row), aka the key of the json element (not the "value")
-  {xx} refer to the value xx of the question, 
-  Alternatively .xx can be used for value with a question name : e.g. $Q1.1 

Question name and response can be used together to refer to another question : 

To sum up :  
- $Q1{1}       : Q1 response with value '1'
- $Q1.1        : Q1 with response '1'
- '[Yes]'      : Response labelled "Yes"
- $Q2[No]      : Question Q2 with response "No"
- $Q1#option_1 : Question Q1, with response in with json key 'option_1' (no necessarily the 'value' to store for this response).s
### Responses

Keys in options list are only to be used as local identifier (like database id)

Define possible response for a question input element (single, multiple, )

Fields:
- **text** : response label
- **comment** : Comment about interpretation or presentation of item. Can be a string or an array of strings.
- **value** : value use to identify this value in the output data model (key, value, or to infer field name)
- **extra** : data name of the question to be used as extra field (see below).
- **description**: Textual description to be shown to the user to give more explanation.
- **platforms**: list of platforms (country code in upper case, e.g. 'UK') or 'all' if it's a core question (expected to be every where).

**Extra Field**: Extra field (aka "open field") was a way to implement sub question attached to an input element (like a checkbox) to enable data enter of an extra information. 
Common usage was the "Other" field. It was not presented as a sub question but as a extra input alongside the checkbox. It was implemented directly in the question as an optional extra input in the old model. The description refers to the extra element as a question itself to avoid this exception in the description model. The "extra" field allow to link both questions with the data_name of this sub question.
This description doesn't fix how this kind of field should be presented in a survey implementation.

## Matrix rows/columns

Fields:
- **text** : response label
- **comment** : Comments about interpretation or presentation of item. Can be a string or an array of strings.
- **value** : value use to identify this value in the output data model (key, value, or to infer field name)
- **platforms**: list of platforms (country code in upper case, e.g. 'UK') or 'all' if it's a core question (expected to be every where).

## Comment
Each comment field can be a string or an array of string (each will be visible as separated block, in order)