"""
exceptions.py

The exceptions module contains the exception classes used by the MarkyBrief system to
communicate errors encountered during the summarisation process. The errors are delivered
using the exception classes:
    - :class: `markybrief.ElementException` - used to communicate element processing errors.
    - :class: `markybrief.BrieferException` - used to communicate general summarisation
        errors.
  
Authors:
  ibrathesheriff (thesheriff@ibrathesheriff.com)
"""

class ElementException(Exception):
    """
    Represents element processing errors like trying to render HTML or markdown for
    elements that are not headings.

    :param str element_type: the type of the element e.g. 'text'
    :param str message: the error message to display when the exception is raised
    """
    def __init__(self, element_type, message) -> None:
        # inherit from the Exception class
        super().__init__(message)
        self._element_type = element_type
        self._message = message
        self._error_name = "BrieferError"

    def __str__(self) -> str:
        """
        The string representation of the exception and it's information.

        :return: the error information as a string
        :rtype: str
        """
        return "%s: %s for <%s>" % (self._error_name, self._message, self._element_type)

class BrieferException(Exception):
    """
    Represents general errors encountered by the briefer during the summarisation process
    like:
        - source document not found
        - invalid summarisation format provided

    :param str message: the error message to display when the exception is raised
    """
    def __init__(self, message) -> None:
        # inherit from the Exception class
        super().__init__(message)
        self._message = message
        self._error_name = "BrieferError"

    def __str__(self) -> str:
        """
        The string representation of the exception and it's information.

        :return: the error information as a string
        :rtype: str
        """
        return "%s: %s" % (self._error_name, self._message)

