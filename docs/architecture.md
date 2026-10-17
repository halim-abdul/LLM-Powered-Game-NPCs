# Architecture

The engine owns orchestration, not the game simulation. A turn validates input, derives allowed actions from an immutable world snapshot, retrieves evidence, calls a provider, validates its result, then stores the completed exchange.

## Contracts

Providers implement `generate(system, context)` and return a dictionary with string fields `dialogue` and `action`. Model actions are suggestions. A provider may raise transport or parsing errors; the engine returns a deterministic talk fallback for those failures. Programming errors outside the documented exception set propagate.

Characters have stable IDs, display names, personality text and goals. Stable IDs, rather than display names, isolate memory. Player IDs must come from the host's authenticated session in a multiplayer integration.

## Retrieval

Lore uses lowercase word-set overlap with the player query. Positive matches are sorted by overlap, then ID for deterministic ties. Conversation history uses overlap and recency, selecting from at most 200 recent rows for that character/player. This is lexical retrieval-augmented prompting, not vector search.

The current memory representation preserves raw turns. It does not automatically infer facts, summarize relationships, resolve conflicting beliefs or forget old rows. `Memory.forget(npc, player)` explicitly removes a partition.

## State and failure boundaries

No SQLite transaction is held during a remote request. A failed persistence write propagates to the host. A successful provider response followed by a storage failure therefore does not constitute a completed turn. Concurrent requests for one player should be serialized by the host.

World state is not modified by generation. The allowlist excludes trade during danger, even if the shop is open. Recheck preconditions against authoritative game state before applying any suggestion.
