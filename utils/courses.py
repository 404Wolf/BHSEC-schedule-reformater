import re
from dataclasses import dataclass, field
from string import ascii_uppercase


import pandas


class Courses(list):
    """
    A list of courses.

    This class provides a method to import courses from a Pandas.DataFrame object which
    automatically parses the courses from the df and adds them to the list.

    Methods:
        types: Obtain a list of all course types.
        from_df: Import courses from a Pandas DataFrame.
    """

    def __init__(self, courses):
        super().__init__(courses)

    def types(self):
        """
        Obtain a list of all course types.
        """
        return list(set([course.type for course in self]))

    def all_unparsed(self):
        """
        Obtain a list of all unparsed strings of the courses.
        """
        return [course.unparsed for course in self]

    def by_unparsed(self, unparsed):
        """
        Obtain a course contained in the list by its unparsed string.

        Args:
            unparsed (str): The unparsed string of the course to obtain.

        Returns:
            Course: The course with the unparsed string that is contained in the list.
        """
        for course in self:
            if course.unparsed == unparsed:
                return course

    @classmethod
    def from_df(cls, df: pandas.DataFrame):
        """
        Import courses from a Pandas DataFrame.

        Args:
            df (pandas.DataFrame): The DataFrame to import courses from.

        Returns:
            Courses: The list of courses.
        """
        courses = []
        for course in df.keys():
            # If a course does not have "[" in it, it is not a course, but rather is
            # a free response question.
            if "[" in course:
                # Only include what is in brackets for the course name
                course_string = course[course.find("[") + 1 : course.find("]")]
                # Remove the * from the course string
                course_string = course_string.replace("*", "")
                if "tutorial" in course.lower():
                    courses.append(
                        Course(
                            name=course_string.title(),
                            teachers=None,
                            type=course_string.split("in ")[1],
                            bard_code=None,
                            doe_code=None,
                            credits=None,
                            unparsed=course,
                        )
                    )
                else:
                    # Add the course to the list of courses
                    courses.append(Course.from_string(course_string, unparsed=course))
        return cls(courses)


@dataclass(frozen=True)
class Course:
    """
    A course.

    This class provides a method to import a course from a string.

    Attributes:
        name (str): The name of the course.
        type (str): The type of the course.
        teachers (str): The teachers of the course.
        bard_code (str): The BARD code of the course.
        doe_code (str): The DOE code of the course.
        credits (int): The number of credits the course is worth.
        unparsed (str): The unparsed string of the course.
    """

    name: str
    type: str
    teachers: str | None
    bard_code: str | None
    doe_code: str | None
    credits: int | None
    unparsed: str | None = field(default=None, repr=False)

    _regex = re.compile(
        r"^([A-Z]+)\s([\d/X]+)\s(.+)\s\((\d)\scredits?\)\s([A-Z]+\d+[A-Z]+)?\s?(.+)$"
    )

    def __str__(self):
        return f"{self.name}, {self.teachers}. [{self.type}:{self.doe_code}]"

    @classmethod
    def from_string(cls, string, unparsed=None):
        """
        Import a course from a course string.

        Course string format should be as follows:
        "TYPE BARD_CODE NAME (X credits) DOE_CODE TEACHERS"
        - or -
        "TYPE BARD_CODE NAME (X credits) TEACHERS"

        Args:
            string (str): The course string to parse.
        """
        parsed = cls._regex.findall(string)[0]

        return cls(
            type=parsed[0],
            bard_code=parsed[1],
            name=parsed[2],
            credits=parsed[3],
            doe_code=parsed[4] if parsed[4] != "" else None,
            teachers=parsed[5],
            unparsed=string if unparsed is None else unparsed,
        )
