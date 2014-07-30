# coding: utf-8

__author__ = 'yetone'

from StringIO import StringIO
from PIL import Image as Img
from libs.pysicle import GifInfo, Gifsicle
import logging

logger = logging.getLogger()


class Image(object):

    ANTIALIAS = Img.ANTIALIAS

    def __init__(self, fp, mode='r'):
        img = Img.open(fp, mode)
        self.img = img
        self.format = img.format
        self.is_gif = img.format.lower() == 'gif'
        self.gi = GifInfo()
        self.gf = Gifsicle()
        self.fp = fp
        self.size = img.size
        self.filename = img.filename
        self.tmp = None

    def get_raw(self):
        raw = self.fp
        if isinstance(self.fp, str):
            f = open(self.fp, 'rb')
            raw = f.read()
            f.close()
        elif isinstance(self.fp, StringIO):
            raw = self.fp.getvalue()
        return raw

    def resize(self, size, resample=Img.ANTIALIAS):
        if self.is_gif:
            width, height = size
            self.gi.resize_gif(width, height)
        self.img = self.img.resize(size, resample)
        return self

    def crop(self, box=None):
        if self.is_gif:
            x, y, w, h = box
            self.gi.crop_gif_bywh((x, y), (w, h))
        self.img = self.img.crop(box)
        return self

    def save(self, fp, format=None, **params):
        if self.is_gif:
            try:
                raw = self.tmp or self.get_raw()
                data = self.gf.convert_with_pipe(self.gi, raw)
                f = open(fp, 'wb')
                f.write(data)
                f.close()
            except Exception:
                logger.info('gif can not save. fp: %s' % fp)
                self.img.save(fp, format, **params)
        else:
            self.img.save(fp, format, **params)

    @staticmethod
    def open(fp, mode='r'):
        return Image(fp, mode)
