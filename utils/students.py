from dataclasses import dataclass
from math import isnan
from typing import Dict, List, Tuple

import pandas

from utils import Course


class Students(list):
    def __init__(self, students):
        super().__init__(students)

    @classmethod
    def from_df(cls, df: pandas.DataFrame, courses):
        """
        Import students from a Pandas DataFrame.

        Args:
            df (pandas.DataFrame): The DataFrame to import students from.
            courses (Courses): The course list.

        Returns:
            Students: The list of students.
        """
        students = []
        for index, student in df.iterrows():
            student_first_name = student["First Name"]
            student_last_name = student["Last Name"]
            student_email = student["Email Address"]
            student_advisor = student["Advisor (last name of academic advisor)"]
            student_courses = {}

            for unparsed_course in courses.all_unparsed():
                course = courses.by_unparsed(unparsed_course)
                course_ranking = student[course.unparsed]
                course_ranking = 0 if isnan(course_ranking) else int(course_ranking)

                if course.type in courses.types():
                    if course.type in student_courses:
                        if course_ranking in student_courses[course.type]:
                            student_courses[course.type][course_ranking].append(course)
                        else:
                            student_courses[course.type][course_ranking] = [course]
                    else:
                        student_courses[course.type] = {course_ranking: [course]}

            student = Student(
                name=(student_first_name, student_last_name),
                email=student_email,
                advisor=student_advisor,
                courses=student_courses,
            )
            students.append(student)

        return cls(students)


@dataclass(frozen=True)
class Student:
    """
    A student.

    Attributes:
        name (Tuple[str, str]): The student's name. (first_name, last_name)
        email (str): The student's email address.
        advisor (str): The student's advisor.
        courses (Dict[str, List[Course]]): {<course-type>: {<ranking>: [courses]}
    """

    name: Tuple[str, str]
    email: str
    advisor: str
    courses: Dict[str, Dict[int, List[Course]]]

    def pretty_preferences(self):
        """
        Obtain a list of pretty strings of the student's course preference.
        This outputs a dict in the format:
        ```
        {
            <course-type>: <pretty-string>,
            <course-type>: <pretty-string>,
            <course-type>: <pretty-string>,
        }
        ```

        The format of the pretty strings is:
        ```
        Type:
            Ranking:
                [rank] CourseName, DOE-Code
                [rank] CourseName, DOE-Code
                [rank] CourseName, DOE-Code
        Type2:
            etc.
        ```

        Returns:
            Dict[str, str]: The list of strings. {<course-type>: <pretty-string>}
        """
        preferences = {}
        sorted_courses = dict(sorted(tuple(self.courses.items())))

        for course_type in sorted_courses:
            pretty_string = f"{course_type}:\n"
            for ranking in self.courses[course_type]:
                if ranking == 0:
                    continue

                if ranking == 1:
                    suffix = "st"
                elif ranking == 2:
                    suffix = "nd"
                elif ranking == 3:
                    suffix = "rd"
                else:
                    suffix = "th"

                pretty_string += f"  {ranking}{suffix} Choices:\n"
                for course in self.courses[course_type][ranking]:
                    pretty_string += (
                        f'    - "{course.name}" ({course.doe_code})\n'
                    )
                pretty_string += "\n"
            preferences[course_type] = pretty_string
        return preferences
