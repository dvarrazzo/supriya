# -*- encoding: utf-8 -*-
import abc
from supriya.tools.synthdeftools.UGen import UGen


class MultiOutUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_count',
        '_output_proxies',
        )

    ### INTIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        rate=None,
        special_index=0,
        channel_count=1,
        **kwargs
        ):
        self._channel_count = int(channel_count)
        UGen.__init__(
            self,
            rate=rate,
            special_index=special_index,
            **kwargs
            )

    ### SPECIAL METHODS ###

    def __len__(self):
        return self.channel_count

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return [self.rate] * len(self)

    @classmethod
    def _new_expanded(
        cls,
        rate=None,
        special_index=0,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        ugen = super(MultiOutUGen, cls)._new_expanded(
            rate=rate,
            special_index=special_index,
            **kwargs
            )
        output_proxies = []
        if isinstance(ugen, synthdeftools.UGen):
            output_proxies.extend(ugen[:])
        else:
            for x in ugen:
                output_proxies.extend(x[:])
        if len(output_proxies) == 1:
            return output_proxies[0]
        result = synthdeftools.UGenArray(output_proxies)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def outputs(self):
        return [self.rate for _ in range(len(self))]