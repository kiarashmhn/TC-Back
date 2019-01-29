from flask import current_app


class SearchHandler():

    @staticmethod
    def add_to_index(index, model):
        if not current_app.elasticsearch:
            return
        payload = {}
        for field in model.__searchable__:
            payload[field] = getattr(model, field)
        current_app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                                        body=payload)

    @staticmethod
    def remove_from_index(index, model):
        if not current_app.elasticsearch:
            return
        current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)
