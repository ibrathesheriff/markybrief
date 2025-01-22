"""
test_briefer.py

Contains pytest test cases to test MarkyBrief briefer system.
  
Authors:
  ibrathesheriff (thesheriff@ibrathesheriff.com)
"""
from markybrief.briefer import Briefer
from markybrief.exceptions import BrieferException
import pytest
import os

LEN_SUBTRACTOR = len("tests")
PROJECT_PATH = os.path.dirname(__file__)[:len(os.path.dirname(__file__))-LEN_SUBTRACTOR]

def test_brief_parameters_1():
    # check if the system catches the file does not exist
    with pytest.raises(BrieferException):
        brief = Briefer()
        # file does not exist
        output = brief.brief(PROJECT_PATH + "example_docs/does-not-exist.md")

def test_brief_parameters_2():
    # check if the system catches an invalid summarisation format i.e. not markdown or html
    with pytest.raises(BrieferException):
        brief = Briefer()
        # file does not exist
        output = brief.brief(PROJECT_PATH + "example_docs/example1.md", "pdf")

def test_markdown_headings_1():
    # check if the correct number of markdown heading is created
    brief = Briefer()

    output = brief.brief(PROJECT_PATH + "example_docs/example1.md")

    assert output.count("#") == 25

def test_markdown_headings_2():
    # check if the correct number of markdown heading is created
    brief = Briefer()

    output = brief.brief(PROJECT_PATH + "example_docs/example3.html")

    assert output.count("#") == 25

