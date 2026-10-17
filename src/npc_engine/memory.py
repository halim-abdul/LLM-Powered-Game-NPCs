"""SQLite memory isolated by NPC and player; bounded retrieval."""
import re
import sqlite3


def words(text):
    return set(re.findall(r"\w+", text.casefold())) - {
        "the", "a", "an", "is", "are", "where", "what", "of", "to", "in",
        "and", "can", "you", "me", "it", "i", "do", "did", "we", "about",
    }


class Memory:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS memories "
            "(id INTEGER PRIMARY KEY, npc TEXT, player TEXT, content TEXT)"
        )

    def add(self, npc, player, content):
        with self.db:
            self.db.execute(
                "INSERT INTO memories(npc,player,content) VALUES(?,?,?)",
                (npc, player, content),
            )

    def recall(self, npc, player, query, limit=4):
        if limit < 0:
            raise ValueError("limit must be nonnegative")
        rows = self.db.execute(
            "SELECT id,content FROM memories WHERE npc=? AND player=? "
            "ORDER BY id DESC LIMIT 200", (npc, player)
        ).fetchall()
        tokens = words(query)
        ranked = sorted(rows, key=lambda r: (len(tokens & words(r[1])), r[0]), reverse=True)
        return [content for _, content in ranked[:limit]]

    def forget(self, npc, player):
        with self.db:
            self.db.execute("DELETE FROM memories WHERE npc=? AND player=?", (npc, player))

    def close(self):
        self.db.close()
