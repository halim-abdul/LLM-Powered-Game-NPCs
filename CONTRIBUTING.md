# Contributing

Keep changes focused and explain the observed problem and resulting behavior. Include a runnable example for new public interfaces.

Run `python -m unittest discover -s tests -v` and the offline CLI before submitting. Add regression coverage when changing memory isolation, action constraints or provider parsing. Live tests must be opt-in and must never require committed credentials.

Do not commit real player conversations, API keys, generated databases or unverified benchmark claims. Keep dependency additions justified and document their operational tradeoffs.
