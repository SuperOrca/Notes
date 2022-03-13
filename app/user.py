import json
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .models import Item, Note


user = Blueprint("user", __name__)


@user.route("/notes")
@login_required
def notes():
    return render_template("notes.html")


@user.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@user.route("/notes/<int:note_id>")
@login_required
def items(note_id):
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            return render_template("items.html", note=note)
        else:
            flash("You do not have permission to view this note.", category="danger")
    else:
        flash("Note not found.", category="danger")

    return redirect(url_for("user.notes"))


@user.route("/item/new/<int:note_id>", methods=["GET", "POST"])
@login_required
def new_item(note_id):
    if request.method == "POST":
        note = Note.query.get(note_id)
        if note:
            if note.user_id == current_user.id:
                content = request.form.get("content")
                if content:
                    item = Item(content=content)
                    note.items.append(item)
                    db.session.commit()

                    print(note.items)
                    return redirect(url_for("user.items", note_id=note_id))
                else:
                    flash("Please enter content.", category="danger")
            else:
                flash(
                    "You do not have permission to edit this note.", category="danger"
                )
        else:
            flash("Note not found.", category="danger")
    return render_template("new_item.html")


@user.route("/item/delete", methods=["POST"])
@login_required
def delete_item():
    data = json.loads(request.data)
    note_id = data.get("note_id")
    item_id = data.get("item_id")
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            item = Item.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
            else:
                flash("Item not found.", category="danger")
        else:
            flash("You do not have permission to delete this note.", category="danger")
    else:
        flash("Note not found.", category="danger")
    return jsonify({})


@user.route("/item/edit/<int:note_id>/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(note_id, item_id):
    if request.method == "POST":
        content = request.form.get("content")

        note = Note.query.get(note_id)

        if note:
            if note.user_id == current_user.id:
                item = Item.query.get(item_id)
                if content:
                    item.content = content
                    db.session.commit()
                else:
                    flash("Please enter content.", category="danger")
            else:
                flash(
                    "You do not have permission to edit this note.", category="danger"
                )
        else:
            flash("Note not found.", category="danger")

        return redirect(url_for("user.items", note_id=note_id))

    return render_template("edit_item.html")


@user.route("/notes/new", methods=["GET", "POST"])
@login_required
def new_note():
    if request.method == "POST":
        name = request.form.get("name")

        if name:

            note = Note(name=name)

            current_user.notes.append(note)
            db.session.commit()
            return redirect(url_for("user.notes"))
        else:
            flash("Please enter an name.", category="danger")

    return render_template("new_note.html")


@user.route("/notes/delete", methods=["POST"])
@login_required
def delete_note():
    data = json.loads(request.data)
    note_id = data.get("note_id")
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            for item in note.items:
                db.session.delete(item)
            db.session.delete(note)
            db.session.commit()
        else:
            flash("You do not have permission to edit this note.", category="danger")
    else:
        flash("Note not found.", category="danger")

    return jsonify({})


@user.route("notes/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    if request.method == "POST":
        name = request.form.get("name")

        note = Note.query.get(note_id)

        if note:
            if note.user_id == current_user.id:
                if name:
                    note.name = name
                    db.session.commit()
                else:
                    flash("Please enter an name.", category="danger")
            else:
                flash(
                    "You do not have permission to edit this note.", category="danger"
                )
        else:
            flash("Note not found.", category="danger")

        return redirect(url_for("user.notes"))

    return render_template("edit_note.html")
