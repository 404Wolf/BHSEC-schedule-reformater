import json
from pprint import pprint

import pandas
import xlsxwriter

import utils


with open("config.json") as f:
    config = json.load(f)


def main():
    with open("input.csv") as f:
        inputs = pandas.read_csv(f)

    courses = utils.Courses.from_df(inputs)
    students = utils.Students.from_df(inputs, courses)

    workbook = xlsxwriter.Workbook("output.xlsx")
    worksheet = workbook.add_worksheet("PageStyle_Sheet1")

    worksheet.write(0, 0, "SchoolDbn")
    worksheet.write(0, 1, "SchoolYear")
    worksheet.write(0, 2, "TermId")
    worksheet.write(0, 3, "StudentId")
    worksheet.write(0, 4, "LastName")
    worksheet.write(0, 5, "FirstName")
    worksheet.write(0, 6, "OffClass")
    worksheet.write(0, 7, "Gender")
    for i in range(15):
        worksheet.write(0, 8 + i, f"Course{i + 1}")

    for row_index, student in enumerate(students):
        row_data = (
            config["School ID"],
            config["School Year"],
            config["Term ID"],
            "<StudentID>",
            student.name[1].upper(),
            student.name[0].upper(),
            "<OffClass>",
            "<Gender>",
        )

        for column_index, item in enumerate(row_data):
            worksheet.write(row_index + 1, column_index, item)

        column_index_offset = 0
        for column_index, (course_type, pretty_course) in enumerate(
            student.pretty_preferences().items(), start=8
        ):
            column_index -= column_index_offset

            # Write the DOE code of their top choice
            if 1 in student.courses[course_type]:
                top_choice_course = student.courses[course_type][1][0]
                if top_choice_course.doe_code is None:
                    if "tutorial" in top_choice_course.name.lower():
                        top_choice = "tutorial"
                    else:
                        top_choice = "other"
                else:
                    top_choice = top_choice_course.doe_code
            else:
                column_index_offset += 1
                continue
            worksheet.write(row_index + 1, column_index, top_choice)

            # Comment all of their other choices
            worksheet.write_comment(
                row_index + 1,
                column_index,
                pretty_course,
                {"x_scale": 1.4, "y_scale": 4},
            )

    workbook.close()


if __name__ == "__main__":
    main()
