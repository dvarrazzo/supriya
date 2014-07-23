# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class OutputProxy(UGenMethodMixin):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_output_index',
        '_source',
        )

    ### INITIALIZER ###

    def __init__(self, source=None, output_index=None):
        from supriya import synthdeftools
        assert isinstance(source, synthdeftools.UGen)
        assert isinstance(output_index, int)
        self._output_index = output_index
        self._source = source

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self

    ### PRIVATE METHODS ###

    def _get_output_number(self):
        return self._output_index

    def _get_source(self):
        return self._source

    ### PUBLIC PROPERTIES ###

    @property
    def rate(self):
        return self.source.rate

    @property
    def output_index(self):
        return self._output_index

    @property
    def source(self):
        return self._source