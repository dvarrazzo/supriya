# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools

"""
SynthDef("clap", {
    arg outBus=0, amp = 0.5;
    var env1, env2, out, noise1, noise2;

    env1 = EnvGen.ar(
        Env.new(
            [0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0.001, 0.013, 0, 0.01, 0, 0.01, 0, 0.03],
            [0, -3, 0, -3, 0, -3, 0, -4],
            )
        );
    env2 = EnvGen.ar(
        Env.new(
            [0, 1, 0],
            [0.02, 0.3],
            [0, -4]
            ),
        doneAction:2,
        );

    noise1 = WhiteNoise.ar(env1);
    noise1 = HPF.ar(noise1, 600);
    noise1 = BPF.ar(noise1, 2000, 3);

    noise2 = WhiteNoise.ar(env2);
    noise2 = HPF.ar(noise2, 1000);
    noise2 = BPF.ar(noise2, 1200, 0.7, 0.7);

    out = noise1 + noise2;
    out = out * 2;
    out = out.softclip * amp;

    Out.ar(outBus, out.dup);
})
"""

def _build_clap_synthdef():

    builder = synthdeftools.SynthDefBuilder(
        out=0,
        amplitude=0.5,
        )

    with builder:

        envelope_one = synthdeftools.Envelope(
            amplitudes=(0, 1, 0, 1, 0, 1, 0, 1, 0),
            durations=(0.001, 0.013, 0, 0.01, 0, 0.01, 0, 0.03),
            curves=(0, -3, 0, -3, 0, -3, 0, -4),
            )
        envelope_generator_one = ugentools.EnvGen.ar(
            envelope=envelope_one,
            )

        envelope_two = synthdeftools.Envelope(
            amplitudes=(0, 1, 0),
            durations=(0.02, 0.3),
            curves=(0, -4),
            )
        envelope_generator_two = ugentools.EnvGen.ar(
            envelope=envelope_two,
            done_action=2,
            )

        noise_one = ugentools.WhiteNoise.ar() * envelope_generator_one
        noise_one = ugentools.HPF.ar(
            source=noise_one,
            frequency=600,
            )
        noise_one = ugentools.BPF.ar(
            source=noise_one,
            frequency=2000,
            reciprocal_of_q=3,
            )

        noise_two = ugentools.WhiteNoise.ar() * envelope_generator_two
        noise_two = ugentools.HPF.ar(
            source=noise_two,
            frequency=1000,
            )
        noise_two = ugentools.BPF.ar(
            source=noise_two,
            frequency=1200,
            reciprocal_of_q=0.7,
            )
        noise_two = noise_two * 0.7

        result = noise_one + noise_two
        result = result * 2
        result = synthdeftools.Op.softclip(result)
        result = result * builder['amplitude']

        ugentools.Out.ar(
            bus=builder['out'],
            source=(result, result),
            )

    synthdef = builder.build()
    return synthdef

clap = _build_clap_synthdef()

__all__ = (
    'clap',
    )
