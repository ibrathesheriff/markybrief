"""
briefer.py

The briefer module contains the :class: `markybrief.Briefer` which is used to encapsulate the
process of summarising a markdown or HTML document i.e. providing a brief version. It is
supported by the following classes:
  - Element - represents a document element i.e. HTML tag
  - Section - represents a collection of document elements that form a content section.

The :class: `markybrief.Briefer` summarise the document into 
  
Authors:
  ibrathesheriff (thesheriff@ibrathesheriff.com)
"""

from summarizer import Summarizer
from bs4 import BeautifulSoup
import markdown
import os

from markybrief.exceptions import ElementException, BrieferException

VALID_FORMATS = ["markdown", "html"]
HEADING_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
HTML_SUMMARY = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%s</title>
</head>
<body>
    %s
</body>
</html>
"""

class _Element:
    """
    Provides an object representation of a element in the document. The information
    of the element is stored as a key-value pair of the element type and textual
    information of the element.

    :param `bs4.Tag` soup_element: BeautifulSoup object to extract the element information from
    """
    def __init__(self, soup_element) -> None:
        if isinstance(soup_element, str):
            self._element_type = "text"
            self._text = soup_element
        elif soup_element.name in HEADING_TAGS:
            self._element_type = soup_element.name
            self._text = soup_element.get_text()
        else:
            self._element_type = "text"  # other elements follow under the text bracket
            self._text = soup_element.get_text()

    def is_heading(self) -> bool:
        """
        Determine if this element is associated with a HTML heading tag.

        :return: True if the element is associated with a HTML heading, False otherwise
        :rtype: bool
        """
        return self._element_type in HEADING_TAGS

    def get_text(self) -> str:
        """
        Returns the textual information of this element.

        :return: the textual information of the element
        :rtype: str
        """
        return self._text
    
    def get_markdown(self) -> str:
        """
        Convert the following element to a Markdown element/section.

        :return: markdown text version of the element
        :rtype: str
        """
        if not self.is_heading():
            raise ElementException(self._element_type,
                                   "Markdown render not supported for this element")
        hashes = int(self._element_type[1]) * "#"
        return hashes + " " + self._text + "\n"

    def get_html(self) -> str:
        """
        Convert the following element to a HTML element.

        :return: HTML representation of the element
        :rtype: str
        """
        if not self.is_heading():
            raise ElementException(self._element_type,
                                   "HTML render not supported for this element")
        html_tag = "<%s>%s</%s>" % (self._element_type, self._text, self._element_type)
        return html_tag
    
    def render(self, format) -> None:
        """
        Converts the element to it's HTML or Markdown representation.

        :return: HTML or Markdown representation of the element
        :rtype: str
        """
        if format == "markdown":
            return self.get_markdown()
        else:
            return self.get_html()
    
    def __str__(self) -> str:
        """
        Returns a string representation of the element's type and text information.

        :return: string representation of the element.
        :rtype: str
        """
        return "%s: %s" % (self._element_type, self._text)

class _Section:
    """
    Provides a object representation of elements that form a content section in the
    document.
    """
    def __init__(self) -> None:
        self._elements = []  # list to hold Element objects
        self._section_text = ""  # to hold the string representation of the section

    def add(self, element: _Element) -> None:
        """
        Adds the given Element object to the list of section elements.

        :param `briefer._Element` element: the element object to add
        """
        self._elements.append(element)

    def _summarise(self, summary_ratio: float) -> str:
        # returns a summarised version of the content section based on the given ratio
        model = Summarizer()  # Initialise the BERT summarizer
        # Generate the section summary
        summary = model(self._section_text, ratio=summary_ratio)
        return summary

    def generate_summary(self, summary_ratio: float) -> str:
        """
        Generates a summary of the whole content section based on the given summary ratio.

        :param float summary_ratio: the summary to full text ratio to use to determine the
            required text reduction
        """
        for element in self._elements:  # combine the section text
            self._section_text += element.get_text()
        return self._summarise(summary_ratio)

class Briefer:
    """
    This class represents the entire MarkyBrief briefer system. It provides the brief
    method that summarises a given document to provide an overview of a document.

    :param float summary_ratio: the summary to full text ratio to use to determine the
        required text reduction for content sections.
    """
    def __init__(self, summary_ratio=0.2) -> None:
        self._summary_ratio = summary_ratio
        self._doc_soup = None
        self._summary_elements = []
        self._element_collection = []
        self._title = None

    def _process_element_collection(self) -> None:
        # converts the formed cluster of elements that are not a heading into a
        # single content section
        if len(self._element_collection) == 0:  # if there is no formed cluster
            return
        # process the elements and create a section
        new_section = _Section()
        for collection_element in self._element_collection:
            new_section.add(collection_element)
        self._summary_elements.append(new_section)
        self._element_collection = []

    def _parse_html(self) -> None:
        # parses the HTML representation of the document to form the heading elements
        # and content sections.
        start_parsing = False  # used to avoid duplication of the entire text
        skip = False  # used to skip the heading text on the next iteration
        for element in self._doc_soup.descendants:
            if skip:
                skip = False
                continue
            if element.name == "body":
                start_parsing = True
                continue
            # if the parsing process hasn't started skip this iteration
            if not start_parsing:
                continue
            # process for headings
            if element.name is not None and element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                self._process_element_collection()
                temp_heading =_Element(element)
                self._summary_elements.append(temp_heading)
                if self._title is None and element.name == "h1":
                    # set the HTML title for the webpage (used if required)
                    self._title = temp_heading.get_text()
                skip = True  # skip the heading text that is just about to follow
            else:  # for the content of sections
                self._element_collection.append(_Element(element))
        # incase the document ends with a text collection
        self._process_element_collection()

    def _generate_markdown(self) -> str:
        # generates a summary of the document in the form of markdown
        summary = ""
        for element in self._summary_elements:
            if isinstance(element, _Element):
                summary += element.render("markdown")
            else:
                summary += element.generate_summary(self._summary_ratio) + "\n\n"
        return summary

    def _generate_html(self, file_path) -> str:
        # generates a summary of the document in the form of HTML
        summary = ""
        for element in self._summary_elements:
            if isinstance(element, _Element):
                summary += element.render("html") + "\n"
            else:
                summary += "<p>%s</p>\n\n" % element.generate_summary(self._summary_ratio)
        if self._title is None:
            parts = file_path.split("\n")
            if len(parts) == 0:  # paranoid
                self._title = file_path
            else:
                file_name = parts[-1]
                dot_point = file_name.rfind(".")
                if dot_point == -1:
                    self._title = file_name
                else:
                    self._title = file_name[:dot_point]
            self._title = self._title.capitalize()

        return HTML_SUMMARY % (self._title, summary)

    def brief(self, file_path: str, format="markdown") -> str:
        """
        Summarises the given document and returns the summary as a Markdown or HTML string.

        :param str file_path: the file path to the document to be summarised
        :param str format: the format of the summarised version - 'markdown' or 'html'
        :return: the summarised version of the given document as a Markdown or HTML string
        :rtype: str
        """
        if format not in VALID_FORMATS:
            err_message = "MarkyBrief only currently supports %s." % ", ".join(VALID_FORMATS)
            raise BrieferException(err_message)
        
        if not os.path.exists(file_path):
            raise BrieferException("MarkyBrief failed to find the file %s" % file_path)

        with open(file_path, "r") as doc_file:
            html_content = doc_file.read()
            if file_path.endswith(".md"):
                # convert the markdown to HTML
                html_content = markdown.markdown(html_content)
            self._doc_soup = BeautifulSoup(html_content, "html5lib")
            # produce the summary elements
            self._parse_html()
            if format == "markdown":
                return self._generate_markdown()
            else:
                return self._generate_html(file_path)

