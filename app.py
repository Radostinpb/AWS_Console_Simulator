from flask import Flask, render_template, request, redirect, url_for, abort
from database import init_db
from models import Instance

app = Flask(__name__)


@app.before_first_request
def setup():
    init_db()


@app.route("/")
def index():
    instances = Instance.all()
    return render_template("index.html", instances=instances)


@app.route("/instances/create", methods=["GET", "POST"])
def create_instance():
    if request.method == "POST":
        name = request.form.get("name")
        instance_type = request.form.get("instance_type")

        if not name or not instance_type:
            return render_template(
                "create.html",
                error="Името и типът са задължителни.",
            )

        Instance.create(name, instance_type)
        return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/instances/<int:instance_id>")
def instance_details(instance_id):
    instance = Instance.get(instance_id)
    if not instance:
        abort(404)
    return render_template("details.html", instance=instance)


@app.route("/instances/<int:instance_id>/start", methods=["POST"])
def start_instance(instance_id):
    instance = Instance.get(instance_id)
    if not instance:
        abort(404)
    if instance.state != "terminated":
        instance.update_state("running")
    return redirect(url_for("index"))


@app.route("/instances/<int:instance_id>/stop", methods=["POST"])
def stop_instance(instance_id):
    instance = Instance.get(instance_id)
    if not instance:
        abort(404)
    if instance.state == "running":
        instance.update_state("stopped")
    return redirect(url_for("index"))


@app.route("/instances/<int:instance_id>/terminate", methods=["POST"])
def terminate_instance(instance_id):
    instance = Instance.get(instance_id)
    if not instance:
        abort(404)
    if instance.state != "terminated":
        instance.update_state("terminated")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
