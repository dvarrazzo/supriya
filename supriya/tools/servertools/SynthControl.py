# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthControl(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        '_default_value',
        '_name',
        '_range',
        '_rate',
        '_unit',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        name=None,
        range_=None,
        rate=None,
        unit=None,
        value=None,
        ):
        from supriya.tools import synthdeftools
        self._client = client
        self._name = str(name)
        if isinstance(range_, synthdeftools.Range):
            self._range = range_
        else:
            self._range = None
        self._rate = synthdeftools.Rate.from_expr(rate)
        self._unit = unit
        self._value = value
        self._default_value = value

    ### SPECIAL METHODS ###

    def __str__(self):
        return self.name

    ### PUBLIC METHODS ###

    @classmethod
    def from_parameter(cls, parameter, client=None):
        from supriya.tools import synthdeftools
        assert isinstance(parameter, synthdeftools.Parameter)
        name = parameter.name
        range_ = parameter.range_
        rate = synthdeftools.Rate.from_input(parameter)
        unit = parameter.unit
        value = parameter.value
        synth_control = SynthControl(
            client=client,
            name=name,
            range_=range_,
            rate=rate,
            unit=unit,
            value=value,
            )
        return synth_control

    def get(self):
        return self._value

    def reset(self):
        self._value = self._default_value

    def set(self, expr, execution_context=None):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        manager = servertools.CommandManager
        if isinstance(expr, servertools.Bus):
            self._value = expr
            if expr.rate == synthdeftools.Rate.CONTROL:
                message = manager.make_node_map_to_control_bus_message(
                    self.client.client,
                    **{self.name: self._value}
                    )
            else:
                message = manager.make_node_map_to_audio_bus_message(
                    self.client.client,
                    **{self.name: self._value}
                    )
        else:
            self._value = float(expr)
            message = manager.make_node_set_message(
                self.client.client,
                **{self.name: self._value}
                )
        execution_context = execution_context or self.client.client.server
        execution_context.send_message(message)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def name(self):
        return self._name

    @property
    def range_(self):
        return self._range

    @property
    def rate(self):
        return self._rate

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value