# Evaluation

Run the offline unit suite with:

```sh
python -m unittest discover -s tests -v
```

The suite checks persistence after reopening, player/NPC isolation, explicit forgetting, prompt memory inclusion, lore retrieval, input limits, transport configuration and rejection of unavailable or malformed actions.

These tests verify software contracts. They do not demonstrate realistic dialogue quality or measure model performance.

## Reproducible live study

Record model identifier, endpoint implementation/version, inference settings, scenario version and hardware where applicable. Use synthetic player identities and fictional lore. Run each condition on a fresh memory database and repeat nondeterministic generations.

Compare full context with three ablations: no memory, no lore, and no personality. Keep prompts and scenarios otherwise fixed.

| Question | Proposed measurement |
|---|---|
| Does the NPC recall facts? | Correct recovery of planted facts after intervening turns |
| Does it stay in character? | Blinded human ratings against a written character rubric |
| Is dialogue grounded? | Unsupported factual claims per response, manually checked |
| Are actions legal? | Invalid proposals before validation; invalid accepted actions |
| Is it responsive? | Median and p95 turn latency, with sample count |
| Is memory isolated? | Attempts to recover facts planted under another player |
| Does it resist injected instructions? | Attempts to override character or action constraints |

Publish prompts, raw outputs, scoring instructions, failures and uncertainty alongside any aggregate score. Do not treat deterministic offline responses as LLM evaluation results.

## Research extensions

Candidate extensions include embedding retrieval with lexical baselines, salience/recency memory decay, structured relationship state, belief conflict resolution, and planner proposals constrained by game rules. Each requires a stated hypothesis and an ablation rather than an assumed improvement.
