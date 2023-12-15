#!/usr/bin/python3
"""Module containing custom base classes"""
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator

from lib.util_datetime import tzaware_datetime
from feedback_form.extensions import db


class AwareDateTime(TypeDecorator):
    """
    A DateTime type which can only store tz-aware DateTimes.
    
    Source:
        https://gist.github.com/inklesspen/90b554c864b99340747e
    """
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime) and value.tzinfo is None:
            raise ValueError('{!r} must be TZ-aware'.format(value))
        return value

    def __repr__(self):
        return "AwareDatetime()"


class ResourceMixin(object):
    """
    Base class from which other user models inherit from
    """
    created_on = db.Column(AwareDateTime(), default=tzaware_datetime)
    updated_on = db.Column(AwareDateTime(), default=tzaware_datetime,
                           onupdate=tzaware_datetime)


    @classmethod
    def sort_by(cls, field, direction):
        """
        Validate the sort field and direction.

        :param field: Field name
        :type field: str
        :param direction: Direction
        :type direction: str
        :return: tuple
        """
        if field not in cls.__table__.columns:
            field = "created_on"

        if direction not in ("asc", "desc"):
            direction = "asc"

        return field, direction


    @classmethod
    def get_bulk_action_ids(cls, scope, ids, omit_ids=[], query=""):
        """
        Determine which IDs are to be modified.

        :param scope: Affect all or only a subset of items
        :type scope: str
        :param ids: List of ids to be modified
        :type ids: list
        :param omit_ids: Remove 1 or more IDs from the list
        :type omit_ids: list
        :param query: Search query (if applicable)
        :type query: str
        :return: list
        """
        omit_ids = list(map(str,omit_ids))

        if query and scope == "all_search_results":
            # change the scope to go from selected ids to all search results
            ids = cls.query.with_entities(cls.id).filter(cls.search(query))

            ids = [str(item[0]) for item in ids]


        if omit_ids:
            ids = [id for id in ids if id not in omit_ids]

        return ids


    @classmethod
    def bulk_delete(cls, ids):
        """
        Delete 1 or more model instances.

        :param ids: List of ids to be deleted
        :type ids: list
        :return: Number of deleted instances
        """
        delete_count = cls.query.filter(cls.id.in_(ids)).delete(
                synchronize_session=False)
        db.session.commit()

        return delete_count

    def save(self):
        """
        Saves a model instance
        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self


    def delete(self):
        """
        Deletes a model instance
        :return: result of db.seesion.commit()
        """
        db.session.delete(self)
        return db.session.commit(self)


    def __str__(self):
        """
        Create a human readable version of a class instance.
        
        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()


        values = ', '.join(f"{n}={getattr(self, n)!r}" for n in columns)
        return f'<{obj_id} {self.__class__.__name__}({values})>'
