# Integration

Use the Python API inside a prototype or wrap it in your own authenticated service. This repository deliberately has no public HTTP server.

For Unity, Unreal or Godot, a host adapter can send player text and an authoritative world snapshot to a Python service. Return dialogue and a suggested action as JSON. Map allowed action names to engine-owned functions; never execute generated strings as code.

## Deployment responsibilities

- Authenticate the player and derive player IDs on the server.
- Serialize turns for each character/player pair and use a separate memory connection per worker.
- Apply request limits, moderation appropriate to the game, and provider cost budgets.
- Set finite provider timeouts and surface fallback events in host telemetry.
- Treat stored player content as untrusted and define a retention policy.
- Back up SQLite save files and provide explicit deletion via `forget`.
- Protect live endpoint configuration; it is operator-controlled, never player-controlled.

The HTTP adapter uses HTTPS except for loopback development endpoints. It performs one request per turn with no automatic retries. It does not stream, expose usage accounting, or implement circuit breaking. Cancellation, retry policy and distributed storage belong in a production host.

## Troubleshooting

If every live turn falls back, check endpoint compatibility, credentials, installed model and whether the model returns plain JSON without Markdown fences. If lore is missed, inspect query word overlap; paraphrase matching is not implemented. If previous dialogue is absent, check stable character/player IDs and the database path.
