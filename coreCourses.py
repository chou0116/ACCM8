from flask import Blueprint, render_template

coreCoursesBlueprint = Blueprint("coreCourses", __name__, static_folder="static", template_folder="template")

@coreCoursesBlueprint.route("/administrator/corecourses")
def coreCourses():
    return render_template("coreCourses.html")


