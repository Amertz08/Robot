import yaml

from flask import Blueprint, render_template, redirect, url_for, \
                    flash, jsonify, request, abort
from flask_login import login_required, current_user

from forms import AddFacilityForm, DeleteFacilityForm, \
                UpdateFacilityForm, AddLayoutForm
from models import db, Facility
from utils import log_message

dash = Blueprint('dash', __name__)


@dash.route('/', methods=['GET', 'POST'])
@login_required
def index():
    add_form = AddFacilityForm()
    delete_form = DeleteFacilityForm()
    update_form = UpdateFacilityForm()
    facilities = Facility.query.filter_by(acct_id=current_user.acct_id).all()
    ctx = {
        'add_form': add_form,
        'delete_form': delete_form,
        'update_form': update_form,
        'facilities': facilities
    }
    return render_template('dash/index.html.j2', **ctx)

@dash.route('/facility/add', methods=['POST'])
@login_required
def add_facility():
    form = AddFacilityForm()
    if form.validate_on_submit():
        facility = Facility(
            acct_id=current_user.acct_id,
            name=form.name.data
        )
        db.session.add(facility)
        db.session.commit()
        log_message(f'user_id: {current_user.id} added facility: {facility.id}')
        flash('Facility created', 'success')
        return jsonify('OK'), 201
    else:
        return jsonify(form.errors)

@dash.route('/facility/edit', methods=['POST'])
@login_required
def update_facility():
    form = UpdateFacilityForm()
    if form.validate_on_submit():
        facility = Facility.query.filter(
            Facility.acct_id == current_user.acct_id,
            Facility.id == form.facility_id.data
        ).first()
        facility.name = form.name.data
        db.session.add(facility)
        db.session.commit()
        log_message(f'user_id: {current_user.id} updated facility: {facility.id}')
        flash('Facility Updated', 'success')
        return jsonify('OK')
    else:
        return jsonify(form.errors)

@dash.route('/facility/delete', methods=['POST'])
@login_required
def delete_facility():
    form = DeleteFacilityForm()
    if form.validate_on_submit():
        facility = Facility.query.filter(
            Facility.name == form.name.data,
            Facility.acct_id == current_user.acct_id
        ).first()
        db.session.delete(facility)
        db.session.commit()
        flash(f'Facility: {facility.name} deleted', 'danger')
        return jsonify('OK')
    else:
        return jsonify(form.errors)


@dash.route('/facility/<facility_id>/layouts')
@login_required
def layouts(facility_id):
    facility = Facility.query.filter(
        Facility.acct_id == current_user.acct_id,
        Facility.id == facility_id
    ).first()
    if not facility:
        abort(404)

    form = AddLayoutForm()
    form.facility_id.data = facility.id
    ctx = {
        'facility': facility,
        'form': form
    }
    return render_template('dash/layouts.html.j2', **ctx)

@dash.route('/facility/<facility_id>/layouts/add', methods=['GET', 'POST'])
@login_required
def add_layout(facility_id):
    form = AddLayoutForm()
    if form.validate_on_submit():
        return jsonify('OK'), 201
    else:
        return jsonify(form.errors)
