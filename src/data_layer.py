from game.base import GameObject


class Writer:
    def to_dict(self, obj):
        data = None
        match obj:
            case GameObject():
                data = dict(obj.__dict__)
                data["_type"] = obj.__class__.__name__
                data["tile"] = obj.tile.name
        return data
