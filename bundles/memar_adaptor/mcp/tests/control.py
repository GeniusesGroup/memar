#!/usr/bin/env python3
from __future__ import annotations

import importlib.machinery
import importlib.util
import io
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from bundles.memar_adaptor.mcp import control

BUDGET_SECONDS = 10


class PingIsLocal(unittest.TestCase):

    def test_ping_request_returns_an_empty_result_without_server_state(self):
        self.assertEqual(control.answer('{"jsonrpc":"2.0","id":7,"method":"ping"}'), '{"jsonrpc":"2.0","id":7,"result":{}}')

    def test_ping_notification_is_consumed_without_a_response(self):
        self.assertIsNone(control.answer('{"jsonrpc":"2.0","method":"ping"}'))

    def test_null_id_is_a_request_and_is_preserved(self):
        self.assertEqual(control.answer('{"jsonrpc":"2.0","id":null,"method":"ping"}'), '{"jsonrpc":"2.0","id":null,"result":{}}')

    def test_invalid_truthy_params_keep_the_workers_invalid_params_error(self):
        self.assertEqual(control.answer('{"jsonrpc":"2.0","id":"x","method":"ping","params":[1]}'), '{"jsonrpc":"2.0","id":"x","error":{"code":-32602,"message":"the params of a request are an object"}}')

    def test_falsey_params_keep_the_workers_existing_empty_params_semantics(self):
        self.assertEqual(control.answer('{"jsonrpc":"2.0","id":1,"method":"ping","params":[]}'), '{"jsonrpc":"2.0","id":1,"result":{}}')

    def test_notification_with_invalid_params_still_has_no_response(self):
        self.assertIsNone(control.answer('{"jsonrpc":"2.0","method":"ping","params":[]}'))

    def test_other_or_malformed_messages_are_left_for_the_worker(self):
        self.assertIs(control.answer('{"jsonrpc":"2.0","id":1,"method":"tools/list"}'), control.NOT_HANDLED)
        self.assertIs(control.answer('{'), control.NOT_HANDLED)

    def test_keepalive_pings_stay_local_and_a_real_request_is_relayed(self):
        path = Path(__file__).resolve().parents[2] / "cli" / "memar"
        loader = importlib.machinery.SourceFileLoader("memar_bridge_test", str(path))
        bridge = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        loader.exec_module(bridge)
        incoming = io.BytesIO(b'{"jsonrpc":"2.0","id":3,"method":"ping"}\n{"jsonrpc":"2.0","method":"ping"}\n{"jsonrpc":"2.0","id":4,"method":"tools/list"}\n')
        outgoing = io.BytesIO()
        server_answer = '{"jsonrpc":"2.0","id":4,"result":{"tools":[]}}'
        with patch.object(sys, "stdin", SimpleNamespace(buffer=incoming)), patch.object(sys, "stdout", SimpleNamespace(buffer=outgoing)), patch.object(bridge, "ask", return_value={"line": server_answer}) as ask, patch.object(bridge, "await_server", side_effect=AssertionError("resident was unavailable")):
            self.assertEqual(bridge.relay(Path.cwd()), 0)
        ask.assert_called_once()
        self.assertEqual(outgoing.getvalue(), b'{"jsonrpc":"2.0","id":3,"result":{}}\n' + server_answer.encode("utf-8") + b'\n')


if __name__ == "__main__":
    unittest.main()
