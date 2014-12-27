#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Josh Brandoff
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from storjtorrent import Session
from storjtorrent import StorjTorrentError
import pytest
import threading
import multiprocessing


@pytest.fixture(scope='class')
def default_session(request):
    s = Session()

    def fin():
        s.set_alive(False)
    request.addfinalizer(fin)
    return s


class TestSession:

    def session_thread_count(self):
        return [isinstance(thread, multiprocessing.dummy.DummyProcess) for
                thread in threading.enumerate()].count(True)

    @pytest.mark.parametrize('min', [-1, 65526, 'shoe'])
    def test_init_port_min(self, min):
        with pytest.raises(StorjTorrentError):
            Session(port_min=min)

    @pytest.mark.parametrize('min,max',
                             [(80, 70), (80, 65526), (80, 'beatboxing')])
    def test_init_port_max(self, min, max):
        with pytest.raises(StorjTorrentError):
            Session(port_min=min, port_max=max)

    @pytest.mark.parametrize('max_download_rate', [-100, 0])
    def test_init_max_download_rate_less_equal_zero(self, max_download_rate):
        s = Session(max_download_rate=max_download_rate)
        assert s.max_download_rate == -1
        s.set_alive(False)

    def test_init_max_download_rate_greater_zero(self):
        max_download_rate = 500
        s = Session(max_download_rate=max_download_rate)
        assert s.max_download_rate == 1000 * max_download_rate
        s.set_alive(False)

    @pytest.mark.parametrize('max_upload_rate', [-100, 0])
    def test_init_max_upload_rate_less_equal_zero(self, max_upload_rate):
        s = Session(max_upload_rate=max_upload_rate)
        assert s.max_upload_rate == -1
        s.set_alive(False)

    def test_init_max_upload_rate_greater_zero(self):
        max_upload_rate = 500
        s = Session(max_upload_rate=max_upload_rate)
        assert s.max_upload_rate == 1000 * max_upload_rate
        s.set_alive(False)

    def test_init_proxy_host_exists(self, default_session):
        proxy = default_session.session.proxy()
        assert proxy.type is 0
        assert proxy.hostname is ''
        assert proxy.port is 0

    def test_init_proxy_host_not_exists(self):
        s = Session(proxy_host='loveboat.org:8123')
        proxy = s.session.proxy()
        assert proxy.type is 4
        assert proxy.hostname == 'loveboat.org'
        assert proxy.port == 8123
        s.set_alive(False)

    def test_set_alive_from_alive_to_dead(self, default_session):
        default_session.set_alive(False)
        assert default_session.alive is False

    def test_set_alive_from_dead_to_alive(self, default_session):
        default_session.set_alive(False)
        thread_count = self.session_thread_count()
        default_session.set_alive(True)
        assert self.session_thread_count() is thread_count + 1
        assert default_session.alive is True

# test: remove torrent
# test: add torrent w/ bad max connections
# test: add torrent w/ good max connections and seeding
# test: add torrent w/ magnet and seeding/not seeding:
# test: add torrent w/ http and https seeding/not seeding:
# test: add torrent w/ fastresume
# test: add torrent w/ verbose
# test: reannounce
# test: pause
# test: resume
# test: sleep (and see that fastresume written)
# test: get_status returns status
# test: watch_torrents w/ verbose and w/out verbose  for 20 seconds
# test: watch_torrents for handles w/ and w/out metadata (e.g. magnets)