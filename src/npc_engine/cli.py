import argparse
from dataclasses import asdict
import json
import os
from .engine import Character, NPC, World
from .memory import Memory
from .providers import HTTPProvider, OfflineProvider


def main():
    parser = argparse.ArgumentParser(description="Talk to Mira, the village archivist")
    parser.add_argument("--message", default="Where is the old bridge?")
    parser.add_argument("--player", default="traveler")
    parser.add_argument("--db", default="npc-memory.sqlite3")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    provider = OfflineProvider()
    if args.live:
        endpoint, model = os.getenv("NPC_ENDPOINT"), os.getenv("NPC_MODEL")
        if not endpoint or not model:
            parser.error("--live requires NPC_ENDPOINT and NPC_MODEL")
        provider = HTTPProvider(endpoint, model)
    memory = Memory(args.db)
    try:
        npc = NPC(Character("mira", "Mira", "Patient, curious, precise", "Preserve village history"),
                  memory, provider, [
                      {"id": "bridge", "text": "The old bridge lies north of the village; its eastern arch is damaged."},
                      {"id": "market", "text": "The village market opens at sunrise."},
                  ])
        print(json.dumps(asdict(npc.turn(args.player, args.message, World())), indent=2))
    finally:
        memory.close()


if __name__ == "__main__":
    main()
