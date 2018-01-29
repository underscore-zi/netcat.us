from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort, g

module = Blueprint('learn', __name__, url_prefix='/learn')

@module.route("/")
def index():
    flash("Error: The learning section is still under construction.")
    return redirect(url_for("home"))

