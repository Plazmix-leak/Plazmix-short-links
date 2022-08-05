import os

from . import main
from app.core.modules import Link
from flask import abort, render_template, redirect, jsonify


@main.route('/<uri>')
@main.route('/@<nickname>')
def main_route(uri: str = None, nickname=None):
    if nickname is not None:
        return redirect(os.getenv('PLAZMIX_PROFILE_ENDPOINT') + nickname)

    if uri is None:
        return abort(404)

    link = Link.get_from_uri(uri)
    if link is None:
        return abort(404)

    if link.active is False:
        return abort(404)

    if link.redirect_type == "speed":
        link.new_use()
        return redirect(link.real_link)

    return render_template("redirect.html", link=link)


@main.route('/cardjson/<uri>.json')
def card_json_generate(uri: str):
    link = Link.get_from_uri(uri)
    if link is None:
        return abort(404)
    return jsonify({"type": "link",
                    "version": "1.0",
                    "author_name": "Plazmix SLS",
                    "provider_name": "click. this is a cat",
                    "provider_url": "https://tenor.com/view/cute-kitty-best-kitty-alex-cute-pp-kitty-omg-yay-cute"
                                    "-kitty-munchkin-kitten-gif-15917800"})
