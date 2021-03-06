# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class RequestBundle(SupriyaValueObject):
    """
    A Request bundle.

    ::

        >>> request_one = requesttools.BufferAllocateRequest(
        ...     buffer_id=23,
        ...     frame_count=512,
        ...     channel_count=1,
        ...     )
        >>> request_two = requesttools.BufferAllocateRequest(
        ...     buffer_id=24,
        ...     frame_count=512,
        ...     channel_count=1,
        ...     )
        >>> request_bundle = requesttools.RequestBundle(
        ...     timestamp=10.5,
        ...     contents=[request_one, request_two],
        ...     )
        >>> print(format(request_bundle))
        supriya.tools.requesttools.RequestBundle(
            timestamp=10.5,
            contents=(
                supriya.tools.requesttools.BufferAllocateRequest(
                    buffer_id=23,
                    frame_count=512,
                    channel_count=1,
                    ),
                supriya.tools.requesttools.BufferAllocateRequest(
                    buffer_id=24,
                    frame_count=512,
                    channel_count=1,
                    ),
                ),
            )

    ::

        >>> print(format(request_bundle.to_osc_bundle(True)))
        supriya.tools.osctools.OscBundle(
            timestamp=10.5,
            contents=(
                supriya.tools.osctools.OscMessage(
                    '/b_alloc',
                    23,
                    512,
                    1
                    ),
                supriya.tools.osctools.OscMessage(
                    '/b_alloc',
                    24,
                    512,
                    1
                    ),
                ),
            )

    ::

        >>> request_bundle.to_list(True)
        [10.5, [['/b_alloc', 23, 512, 1], ['/b_alloc', 24, 512, 1]]]

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents',
        '_timestamp',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        timestamp=None,
        contents=None,
        ):
        from supriya.tools import requesttools
        self._timestamp = timestamp
        if contents is not None:
            prototype = (requesttools.Request, type(self))
            assert all(isinstance(x, prototype) for x in contents)
            contents = tuple(contents)
        else:
            contents = ()
        self._contents = contents

    ### PUBLIC METHODS ###

    def communicate(self, server=None):
        from supriya.tools import servertools
        server = server or servertools.Server.get_default_server()
        assert isinstance(server, servertools.Server)
        assert server.is_running
        message = self.to_osc_bundle()
        server.send_message(message)

    def to_list(self, with_textual_osc_command=False):
        return self.to_osc_bundle(with_textual_osc_command).to_list()

    def to_osc_bundle(self, with_textual_osc_command=False):
        contents = []
        for x in self.contents:
            if isinstance(x, type(self)):
                contents.append(x.to_osc_bundle(with_textual_osc_command))
            else:
                contents.append(x.to_osc_message(with_textual_osc_command))
        bundle = osctools.OscBundle(
            timestamp=self.timestamp,
            contents=contents,
            )
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        return self._contents

    @property
    def timestamp(self):
        return self._timestamp
