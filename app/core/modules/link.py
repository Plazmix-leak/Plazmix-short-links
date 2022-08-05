from pydantic import BaseModel

from app import db, redis_client
from app.utilits import generation_short_link


class LinkModel(BaseModel):
    id: int = None
    uri: str = None
    owner_id: str
    transitions: int = None
    real_link: str
    disposable: bool = False
    active: bool = True
    redirect_type: str = "default"


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    uri = db.Column(db.String(100), nullable=False, primary_key=True, unique=True)

    owner_id = db.Column(db.String(100), nullable=False)  # site = site:ID | vk = vk:ID | auto = bot:identification
    transitions = db.Column(db.Integer, default=0, nullable=False)
    redirect_type = db.Column(db.Enum("default", "speed"), default="default")
    real_link = db.Column(db.String(500), default="https://plazmix.net", nullable=False)
    disposable = db.Column(db.Boolean, default=False, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    @property
    def model(self) -> LinkModel:
        return LinkModel(id=self.id, uri=self.uri,
                         owner_id=self.owner_id, transitions=self.uses,
                         real_link=self.real_link, disposable=self.disposable,
                         active=self.active)

    @property
    def now_dynamic_usage(self):
        try:
            return int(redis_client.get(f'link_{self.uri}').decode('utf-8'))
        except (ValueError, AttributeError):
            return 0

    def set_dynamic_usage(self, data):
        redis_client.set(f'link_{self.uri}', data)

    @property
    def uses(self):
        return self.now_dynamic_usage + self.transitions

    def new_use(self):
        if redis_client.exists(f"link_{self.uri}") is False:
            self.set_dynamic_usage(0)

        redis_client.incr(f'link_{self.uri}', 1)

    def sync_use(self):
        uses = self.now_dynamic_usage
        self.set_dynamic_usage(0)
        self.transitions += uses
        db.session.commit()

    def new_transitions(self):
        self.new_use()

        if self.disposable is True:
            self.active = False

        db.session.commit()
        self.sync_use()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_model(self, model: LinkModel):
        self.real_link = model.real_link
        self.uri = model.uri
        self.active = model.active
        self.redirect_type = model.redirect_type

        db.session.commit()

    @classmethod
    def get_from_id(cls, link_id: int):
        return cls.query.filter(cls.id == link_id).first()

    @classmethod
    def get_from_uri(cls, uri: str):
        return cls.query.filter(cls.uri == uri).first()

    @classmethod
    def get_all_link_in_owner(cls, owner_id: str):
        return cls.query.filter(cls.owner_id == owner_id).all()

    @classmethod
    def create_link(cls, real_link, owner_id, uri=None, disposable=False):
        uri = uri or generation_short_link(4)
        new = cls(uri=uri, owner_id=owner_id, real_link=real_link, disposable=disposable,
                  active=True)
        db.session.add(new)
        db.session.commit()
        return new

    @staticmethod
    def create_from_model(model: LinkModel):
        return Link.create_link(real_link=model.real_link, owner_id=model.owner_id,
                                uri=model.uri, disposable=model.disposable)
