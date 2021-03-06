# -*- encoding: utf-8 -*-
import unittest
from supriya.tools import nonrealtimetools
from supriya.tools import requesttools


class TestCase(unittest.TestCase):

    def test_Session(self):
        session = nonrealtimetools.Session()
        request = requesttools.BufferAllocateReadChannelRequest(
            buffer_id=1,
            channel_indices=[4, 5],
            file_path=session,
            frame_count=512,
            starting_frame=128,
            )
        assert request.file_path is session
        osc_message = request.to_osc_message(with_textual_osc_command=True)
        assert osc_message.address == '/b_allocReadChannel'
        assert osc_message.contents == (1, session, 128, 512, 4, 5)
