import json
from json import JSONDecodeError

from flask import request, jsonify
from pydantic import ValidationError

from . import api
from .tools import api_methods
from app.core.modules import Link, LinkModel


@api.route('/v1/link/create', methods=['POST'])
@api_methods
def api_create():
    try:
        data = request.get_json(force=True)
    except JSONDecodeError:
        data = {}

    try:
        model = LinkModel.parse_obj(data)
    except ValidationError as ex:
        return jsonify(ex.json())

    new_link = Link.create_from_model(model)
    return jsonify({"result": new_link.model.dict()})


@api.route('/v1/owner/<user_id>', methods=['GET'])
@api_methods
def get_all_user(user_id: str):
    all_this_user = Link.get_all_link_in_owner(user_id)
    return jsonify({"result": [this.model.dict() for this in all_this_user]})


@api.route('/v1/link/<int:link_id>', methods=['GET', 'DELETE', 'PUT'])
@api.route('/v1/link/uri/<link_uri>', methods=['GET', 'DELETE', 'PUT'])
@api_methods
def control_link(link_id: int = None, link_uri: str = None):
    if link_id is None:
        link: Link = Link.get_from_uri(link_uri)
    else:
        link: Link = Link.get_from_id(link_id)

    method = request.method.lower()

    if method == 'get':
        return jsonify({"result": link.model.dict()})
    elif method == 'put':
        try:
            data = request.get_json(force=True)
        except JSONDecodeError:
            data = {}

        try:
            model = LinkModel.parse_obj(data)
        except ValidationError as ex:
            return jsonify(ex.json())

        link.update_from_model(model)
        return jsonify({"result": link.model.dict()})
    elif method == 'delete':
        link.delete()
        return jsonify({"result": "ok"})
    else:
        return jsonify({"result": False, "error": {"code": 403, "msg": "error method"}})


@api.route('/public/link/<uri>', methods=['POST'])
def get_uri(uri):
    link: Link = Link.get_from_uri(uri)
    if link is None:
        return jsonify({"status": "no", "error": {"code": 403, "msg": "error method"}})
    if link.active is False:
        return jsonify({"status": "no", "error": {"code": 403, "msg": "link deactive"}})
    link.new_transitions()
    return jsonify({"status": "ok", "result": link.model.dict(exclude={'transitions',
                                                                       'owner_id',
                                                                       'disposable'}
                                                              )})
