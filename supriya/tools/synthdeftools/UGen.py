# -*- encoding: utf-8 -*-
from __future__ import print_function
import abc
import enum
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class UGen(UGenMethodMixin):
    r'''A UGen.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_antecedents',
        '_calculation_rate',
        '_descendants',
        '_inputs',
        '_output_proxies',
        '_special_index',
        '_synthdef',
        '_width_first_antecedents',
        )

    _argument_specifications = ()

    _unexpanded_argument_names = None

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        calculation_rate=None,
        special_index=0,
        **kwargs
        ):
        from supriya import synthdeftools
        assert isinstance(calculation_rate, synthdeftools.CalculationRate), \
            calculation_rate
        self._calculation_rate = calculation_rate
        self._inputs = []
        self._special_index = special_index
        for i in range(len(self._argument_specifications)):
            argument_specification = self._argument_specifications[i]
            argument_name = argument_specification.name
            argument_value = kwargs.get(argument_name, None)
            argument_value = None
            if argument_name in kwargs:
                argument_value = kwargs[argument_name]
                del(kwargs[argument_name])
            prototype = (
                type(None),
                float,
                int,
                UGen,
                synthdeftools.OutputProxy,
                )
            assert isinstance(argument_value, prototype), argument_value
            argument_specification.configure(self, argument_value)
        if kwargs:
            raise ValueError(kwargs)
        self._antecedents = []
        self._descendants = []
        self._output_proxies = tuple(
            synthdeftools.OutputProxy(self, i)
            for i in range(len(self))
            )
        self._synthdef = None
        self._width_first_antecedents = []

    ### SPECIAL METHODS ###

    def __getattr__(self, attr):
        try:
            object.__getattr__(self, attr)
        except AttributeError:
            for i, argument_specification in enumerate(
                self._argument_specifications):
                if argument_specification.name == attr:
                    return self.inputs[i]
        raise AttributeError

    def __getitem__(self, i):
        return self._output_proxies[i]

    def __len__(self):
        return 1

    def __repr__(self):
        from supriya.tools import synthdeftools
        if self.calculation_rate == synthdeftools.CalculationRate.DEMAND:
            return '{}()'.format(type(self).__name__)
        calculation_abbreviations = {
            synthdeftools.CalculationRate.AUDIO: 'ar',
            synthdeftools.CalculationRate.CONTROL: 'kr',
            synthdeftools.CalculationRate.SCALAR: 'ir',
            }
        string = '{}.{}()'.format(
            type(self).__name__,
            calculation_abbreviations[self.calculation_rate]
            )
        return string

    ### PRIVATE METHODS ###

    def _add_constant_input(self, value):
        self._inputs.append(float(value))

    def _add_ugen_input(self, ugen, output_index=None):
        from supriya import synthdeftools
        if isinstance(ugen, synthdeftools.OutputProxy):
            output_proxy = ugen
        else:
            output_proxy = synthdeftools.OutputProxy(
                output_index=output_index,
                source=ugen,
                )
        self._inputs.append(output_proxy)

    def _collect_constants(self):
        from supriya import synthdeftools
        for input_ in self._inputs:
            if not isinstance(input_, synthdeftools.OutputProxy):
                self.synthdef._add_constant(float(input_))

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.calculation_rate]

    def _get_source(self):
        return self

    def _initialize_topological_sort(self):
        from supriya import synthdeftools
        for input_ in self.inputs:
            if isinstance(input_, synthdeftools.OutputProxy):
                ugen = input_.source
                if ugen not in self.antecedents:
                    self.antecedents.append(ugen)
                if self not in ugen.descendants:
                    ugen.descendants.append(self)
        for ugen in self.width_first_antecedents:
            if ugen not in self.antecedents:
                self.antecedents.append(ugen)
            if self not in ugen.descendants:
                ugen.descendants.append(self)

    def _make_available(self):
        if not self.antecedents:
            if self not in self.synthdef._available_ugens:
                self.synthdef._available_ugens.append(self)

    @classmethod
    def _new(cls, calculation_rate, special_index, **kwargs):
        import sys
        from supriya import synthdeftools
        if sys.version_info[0] == 2:
            import funcsigs
            get_signature = funcsigs.signature
        else:
            import inspect
            get_signature = inspect.signature
        assert isinstance(calculation_rate, synthdeftools.CalculationRate)
        argument_dicts = UGen.expand_arguments(
            kwargs, unexpanded_argument_names=cls._unexpanded_argument_names)
        ugens = []
        signature = get_signature(cls.__init__)
        has_custom_special_index = 'special_index' in signature.parameters
        for argument_dict in argument_dicts:
            if has_custom_special_index:
                ugen = cls(
                    calculation_rate=calculation_rate,
                    special_index=special_index,
                    **argument_dict
                    )
            else:
                ugen = cls(
                    calculation_rate=calculation_rate,
                    **argument_dict
                    )
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return synthdeftools.UGenArray(ugens)

    def _optimize_graph(self):
        pass

    def _remove_antecedent(self, ugen):
        self.antecedents.remove(ugen)
        self._make_available()

    def _schedule(self, out_stack):
        for ugen in reversed(self.descendants):
            ugen._remove_antecedent(self)
        out_stack.append(self)

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, **kwargs):
        from supriya.tools import synthdeftools
        ugen = cls._new(
            calculation_rate=synthdeftools.CalculationRate.AUDIO,
            special_index=0,
            **kwargs
            )
        return ugen

    def compile(self, synthdef):
        def compile_input_spec(i, synthdef):
            from supriya import synthdeftools
            result = []
            if isinstance(i, float):
                result.append(SynthDefinition._encode_unsigned_int_32bit(0xffffffff))
                constant_index = synthdef._get_constant_index(i)
                result.append(SynthDefinition._encode_unsigned_int_32bit(
                    constant_index))
            elif isinstance(i, synthdeftools.OutputProxy):
                ugen = i.source
                output_index = i.output_index
                ugen_index = synthdef._get_ugen_index(ugen)
                result.append(SynthDefinition._encode_unsigned_int_32bit(ugen_index))
                result.append(SynthDefinition._encode_unsigned_int_32bit(output_index))
            else:
                raise Exception('Unhandled input spec: {}'.format(i))
            return bytearray().join(result)
        from supriya.tools.synthdeftools import SynthDefinition
        outputs = self._get_outputs()
        result = []
        result.append(SynthDefinition._encode_string(type(self).__name__))
        result.append(SynthDefinition._encode_unsigned_int_8bit(self.calculation_rate))
        result.append(SynthDefinition._encode_unsigned_int_32bit(len(self.inputs)))
        result.append(SynthDefinition._encode_unsigned_int_32bit(len(outputs)))
        result.append(SynthDefinition._encode_unsigned_int_16bit(int(self.special_index)))
        for i in self.inputs:
            result.append(compile_input_spec(i, synthdef))
        for o in outputs:
            result.append(SynthDefinition._encode_unsigned_int_8bit(o))
        result = bytearray().join(result)
        return result

    @classmethod
    def kr(cls, **kwargs):
        from supriya.tools import synthdeftools
        ugen = cls._new(
            calculation_rate=synthdeftools.CalculationRate.CONTROL,
            special_index=0,
            **kwargs
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def antecedents(self):
        return self._antecedents

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def descendants(self):
        return self._descendants

    @property
    def inputs(self):
        return tuple(self._inputs)

    @property
    def signal_range(self):
        from supriya.tools import synthdeftools
        return synthdeftools.SignalRange.BIPOLAR

    @property
    def special_index(self):
        return self._special_index

    @property
    def synthdef(self):
        return self._synthdef

    @synthdef.setter
    def synthdef(self, synthdef):
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, synthdeftools.SynthDefinition)
        self._synthdef = synthdef

    @property
    def width_first_antecedents(self):
        return self._width_first_antecedents