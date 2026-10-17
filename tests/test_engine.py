import tempfile
import unittest
from pathlib import Path
from npc_engine import Character, Memory, NPC, OfflineProvider, World
from npc_engine.providers import HTTPProvider


class Fixed:
    def __init__(self, value):
        self.value = value
        self.context = None

    def generate(self, system, context):
        self.context = context
        return self.value


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()
        self.addCleanup(self.memory.close)
        self.character = Character("mira", "Mira", "patient", "help")

    def npc(self, provider=None):
        return NPC(self.character, self.memory, provider or OfflineProvider(),
                   [{"id": "bridge", "text": "The bridge is north."}])

    def test_grounded_offline_turn(self):
        reply = self.npc().turn("p", "bridge")
        self.assertIn("north", reply.dialogue)
        self.assertEqual(reply.sources, ("bridge",))
        self.assertFalse(reply.fallback)

    def test_player_and_npc_isolation(self):
        self.memory.add("mira", "a", "secret")
        self.assertEqual(self.memory.recall("mira", "b", "secret"), [])
        self.assertEqual(self.memory.recall("other", "a", "secret"), [])

    def test_persistence_and_forget(self):
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "memory.db")
            first = Memory(path)
            first.add("mira", "p", "bridge")
            first.close()
            second = Memory(path)
            try:
                self.assertEqual(second.recall("mira", "p", "bridge"), ["bridge"])
                second.forget("mira", "p")
                self.assertEqual(second.recall("mira", "p", "bridge"), [])
            finally:
                second.close()

    def test_unavailable_actions_fall_back(self):
        for value in ({"dialogue": "Hello", "action": "trade"},
                      {"dialogue": "", "action": "talk"}, [], None,
                      {"dialogue": "Hello", "action": "execute_shell"}):
            with self.subTest(value=value):
                self.assertTrue(self.npc(Fixed(value)).turn("p", "hello").fallback)

    def test_world_constrains_actions(self):
        provider = Fixed({"dialogue": "Run!", "action": "flee"})
        reply = self.npc(provider).turn("p", "help", World(danger=True, shop_open=True))
        self.assertEqual(reply.action, "flee")
        self.assertNotIn("trade", provider.context["allowed_actions"])

    def test_memory_in_prompt(self):
        self.npc().turn("p", "bridge")
        provider = Fixed({"dialogue": "Welcome back", "action": "talk"})
        self.npc(provider).turn("p", "bridge again")
        self.assertEqual(len(provider.context["memories"]), 1)

    def test_input_bounds(self):
        for text in ("", " " , "a" * 4001):
            with self.assertRaises(ValueError):
                self.npc().turn("p", text)

    def test_transport_validation(self):
        with self.assertRaises(ValueError):
            HTTPProvider("http://example.com/chat", "model")
        HTTPProvider("http://localhost:11434/v1/chat/completions", "model")


if __name__ == "__main__":
    unittest.main()
