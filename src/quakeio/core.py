# Claudio Perez
# 2021
import numpy as np


class GroundMotionEvent(dict):
    """
    Container for a collection of GroundMotionRecord objects
    """
    def __init__(self, records, event_date=None, **kwds):
        dict.__init__(self, **records)
        self.event_date = event_date

    def serialize(self, serialize_data=True) -> dict:
        return {k: v.serialize() for k, v in self.items()}

def rotate_horizontal(angle,x,y,overwrite=True):
    vect = np.asarray([x,y])
    np.matmul(rotation, vect, out = vect)

class GroundMotionRecord(dict):
    """
    A container of GroundMotionComponent objects
    """
    def __init__(self, records: dict = {}, **kwds):
        dict.__init__(self, **records)

    def serialize(self, serialize_data=True) -> dict:
        return {k: v.serialize() for k, v in self.items()}

    def rotate(self, angle=None, rotation=None):
        rx, ry = np.array([
            [ np.cos(angle), np.sin(angle)],
            [-np.sin(angle), np.cos(angle)]
        ]) if not rotation else rotation

        for attr in ["accel", "veloc", "displ"]:
            x = getattr(self["long"], attr)
            y = getattr(self["tran"], attr)
            X = np.array([x,y])
            #x, y = rotate_horizontal(horizontal_angle, x, y)
            x[:] = np.dot(rx, X)
            y[:] = np.dot(ry, X)
            #setattr(self["long"], attr, x)
            #setattr(self["tran"], attr, y)
        return self


class GroundMotionComponent(dict):
    def __init__(self, accel, veloc, displ, meta={}):
        self.accel = accel
        self.displ = displ
        self.veloc = veloc
        dict.__init__(self, **meta)

    def serialize(self, serialize_data=True) -> dict:
        ret = dict(self)
        ret.update(
            {
                **self.accel.serialize("accel", serialize_data=serialize_data),
                **self.veloc.serialize("veloc", serialize_data=serialize_data),
                **self.displ.serialize("displ", serialize_data=serialize_data),
            }
        )
        return ret


class GroundMotionSeries(np.ndarray):
    def __new__(cls, input_array, metadata={}):
        obj = np.asarray(input_array).view(cls)

        for k, v in metadata.items():
            if not hasattr(obj, k):
                setattr(obj, k, v)
        return obj
    def __repr__(self):
        return f"<quakeio.GroundMotionSeries>"
    def serialize(self, key=None, serialize_data=True):
        if key is None:
            key = self.series_type
        attributes = {
            ".".join((key, k)): v for k, v in self.__dict__.items() if k[0] != "_"
        }
        if serialize_data:
            attributes.update({key: list(self)})
        return attributes

    def __array_finalize__(self, obj):
        for k, v in self.__dict__.items():
            setattr(obj, k, v)

    def plot(self, ax=None, fig=None):
        import matplotlib.pyplot as plt

        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(self)

