# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class BufCombN(PureUGen):
    r'''Buffer-based non-interpolating comb delay line unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> buffer_id = 0
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.BufCombN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        BufCombN.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        'maximum_delay_time',
        'delay_time',
        'decay_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        calculation_rate=None,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        PureUGen.__init__(
            self,
            buffer_id=int(buffer_id),
            calculation_rate=calculation_rate,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create an audio-rate buffer-based non-interpolating comb delay
        line.

        ::

            >>> from supriya.tools import ugentools
            >>> buffer_id = 0
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.BufCombN.ar(
            ...     buffer_id=buffer_id,
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            BufCombN.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        source = cls.as_audio_rate_input(source)
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        decay_time=1.0,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        r'''Create a control-rate buffer-based non-interpolating comb delay
        line.

        ::

            >>> from supriya.tools import ugentools
            >>> buffer_id = 0
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.BufCombN.kr(
            ...     buffer_id=buffer_id,
            ...     decay_time=1.0,
            ...     delay_time=0.2,
            ...     maximum_delay_time=0.2,
            ...     source=source,
            ...     )
            BufCombN.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            decay_time=decay_time,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
        return ugen
