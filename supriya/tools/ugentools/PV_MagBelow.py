# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagAbove import PV_MagAbove


class PV_MagBelow(PV_MagAbove):
    """
    Passes magnitudes below threshold.

    ::

        >>> pv_chain = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_below = ugentools.PV_MagBelow(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ...     )
        >>> pv_mag_below
        PV_MagBelow.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'threshold',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        threshold=0,
        ):
        PV_MagAbove.__init__(
            self,
            pv_chain=pv_chain,
            threshold=threshold,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        threshold=0,
        ):
        """
        Constructs a PV_MagBelow.

        ::

            >>> pv_mag_below = ugentools.PV_MagBelow.new(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_below
            PV_MagBelow.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            threshold=threshold,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_MagBelow.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_below = ugentools.PV_MagBelow(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_below.pv_chain
            OutputProxy(
                source=FFT(
                    buffer_id=OutputProxy(
                        source=LocalBuf(
                            frame_count=2048.0,
                            channel_count=1.0,
                            calculation_rate=CalculationRate.SCALAR
                            ),
                        output_index=0
                        ),
                    source=OutputProxy(
                        source=WhiteNoise(
                            calculation_rate=CalculationRate.AUDIO
                            ),
                        output_index=0
                        ),
                    active=1.0,
                    hop=0.5,
                    window_size=0.0,
                    window_type=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def threshold(self):
        """
        Gets `threshold` input of PV_MagBelow.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_below = ugentools.PV_MagBelow(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_below.threshold
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]
