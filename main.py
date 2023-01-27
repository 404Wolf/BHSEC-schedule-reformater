import pandas

import utils


def main():
    courses = []
    with open("input.csv") as f:
        input = pandas.read_csv(f)
        for course in input.keys():
            # If a course does not have "[" in it, it is not a course, but rather is
            # a free response question.
            if "[" in course:
                # Only include what is in brackets for the course name
                course_string = course[course.find("[") + 1 : course.find("]")]
                # Remove the * from the course string
                course_string = course_string.replace("*", "")
                if "tutorial" in course.lower():
                    courses.append(
                        utils.Course(
                            name=course_string.title(),
                            teachers=None,
                            type=course_string.split("in ")[1],
                            bard_code=None,
                            doe_code=None,
                            credits=None,
                        )
                    )
                else:

                    # Add the course to the list of courses
                    courses.append(utils.Course.from_string(course_string))

    # Print the courses
    for course in courses:
        print(course)


if __name__ == "__main__":
    main()
