import pandas

import utils

def main():
    courses = []
    with open("input.csv") as f:
        input = pandas.read_csv(f)
        for course in input.keys():
            # Only include what is in brackets for the course name
            course_string = course[course.find("[") + 1 : course.find("]")]
            # Remove the * from the course string
            course_string.replace("*", "")
            # Add the course to the list of courses
            courses.append(utils.Course.from_string(course_string))


if __name__ == "__main__":
    main()