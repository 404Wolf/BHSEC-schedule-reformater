from dataclasses import dataclass


@dataclass(frozen=True)
class Course:
    name: str
    code: str
    credits: int

    @classmethod
    def from_string(cls, string):
        """
        Import a course from a course string.

        Course string format should be as follows:
        "TYPE BARD_CODE NAME (X credits) DOE_CODE TEACHERS"

        Args:
            string (str): The course string to parse.
        """
        # Split the string into its components.
        components = string.split(" ")

        print(components)
