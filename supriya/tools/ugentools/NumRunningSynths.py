# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class NumRunningSynths(InfoUGenBase):
    r'''Number of running synths info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.NumRunningSynths.ir()
        NumRunningSynths.ir()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        ):
        InfoUGenBase.__init__(
            self,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(cls, **kwargs):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new(
            calculation_rate=calculation_rate,
            **kwargs
            )
        return ugen