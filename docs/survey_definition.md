# Survey Description Format

## Goals

This format is intended purpose of this format is to describe a survey and it's element in order to create documentation and facilitate survey maintenance and migration between legacy influenzanet platform and the new one. It's not as precise as a technical implementation for a survey engine (where a lot of technical spec could be defined).

## Structure

A survey is defined as a set of *Questions*.

### Question

*Question* is a the main element of a survey structure. One question contains textual fields to describe the expected data to be collected.

Common fields:
- **title**: Label of the question as to be presented to the user (after translation). 
- **type** : Kind of Question. Define how the data collection is organized
- **description** : Textual description of the question to the final user
- **data_name**: name to be used to identify the question in the data
- **active** : can be used to indicate the question is inactive (value="false")            
- **comment** : Textual comments about the question for survey designer/scientific aspects ()
- **mandatory**: is the field needs to be mandatory
- **added_at**: date when the question has been added
- **removed_at**: date when the question has been removed
- **data_type**: Can be used to describe the expected type of data to be collected from the data elements (numeric, text, date)
- **rules**: list of rules (textual description tto be applied on this question)

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

### Responses

Keys in options list are only to be used as local identifier (like database id)

Define possible response for a question input element (single, multiple, )

Fields:
- **text** : response label
- **comment** : Comment about interpretation or presentation of item
- **value** : value use to identify this value in the output data model (key, value, or to infer field name)
- **extra** : data name of the question to be used as extra field (see below).

**Extra Field**: Extra field (aka "open field") was a way to implement sub question attached to an input element (like checkbox) to enable data enter of 
an extra information. Common usage was the "Other" field. It was not presented as a sub question but as a extra input alongside the checkbox. It was implemented directly in the question as an optional extra input in the old model. The description refers to the extra element as a question itself to avoid this exception in the description model. The "extra" field allow to link both questions with the data_name of this sub question.
This description doesnt fix how this kind of field should be presented in a survey implementation.


## Matrix rows/columns

Fields:
- **text** : response label
- **comment** : Comments about interpretation or presentation of item
- **value** : value use to identify this value in the output data model (key, value, or to infer field name)

## Comment
Each comment field can be a string or an array of string (each will be visible as separated block, in order)