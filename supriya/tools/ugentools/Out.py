# -*- encoding: utf-8 -*-
import collections
from supriya.tools.synthdeftools.UGen import UGen


class Out(UGen):
    r'''Bus output unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.SinOsc.ar()
        >>> ugentools.Out.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        Out.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        )

    _unexpanded_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        bus=0,
        source=None,
        ):
        UGen.__init__(
            self,
            bus=bus,
            rate=rate,
            )
        if not isinstance(source, collections.Sequence):
            source = [source]
        for single_source in source:
            self._configure_input('source', single_source)

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        source=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        if isinstance(bus, servertools.BusMixin):
            bus = int(bus)
        return cls._new_expanded(
            bus=bus,
            rate=rate,
            source=source,
            )

    @classmethod
    def kr(
        cls,
        bus=0,
        source=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        if isinstance(bus, servertools.BusMixin):
            bus = int(bus)
        return cls._new_expanded(
            bus=bus,
            rate=rate,
            source=source,
            )