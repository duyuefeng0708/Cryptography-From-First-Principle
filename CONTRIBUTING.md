# Contributing

Thanks for your interest in improving these materials. Here's how to help.

## Reporting Issues

Open an issue if you find:
- Wrong math or broken code in a notebook
- A logical jump that's too big (our core goal is zero logical jumps)
- Unclear explanations or missing context
- Rust exercises that don't compile or have wrong expected values

Use the issue templates. Include the module number and file name.

## Adding Content

The biggest areas that need help:

1. **Break/Connect notebooks** for modules that don't have them yet
2. **Visualizations** that make abstract concepts click
3. **Rust exercises** at different difficulty levels
4. **Typo fixes** and wording improvements

## Style Guide

Every notebook follows these principles:

- **One concept per notebook.** If you're tempted to cover two ideas, split it.
- **Concrete first.** Start with Z_7, not abstract group G. Start with a 4-bit field, not GF(2^256).
- **No logical jumps.** Every step must follow from the previous one. If a student has to pause and think "wait, where did that come from?", we failed.
- **Show, don't tell.** Use SageMath code cells to demonstrate, then explain.
- **Exercises build, not test.** Exercises should extend the concept, not quiz rote memory.

Break notebooks follow this structure:
1. Title and module tag
2. "Why This Matters" (1-2 paragraphs)
3. "The Scenario" with concrete small numbers
4. Step-by-step attack with SageMath code cells
5. Cost analysis
6. "The Fix" showing the secure choice
7. Exercises (2-3 variations)
8. Summary with key takeaways

Connect notebooks follow this structure:
1. Title and module tag
2. Introduction tracing module concepts to the real protocol
3. Concrete walkthrough with SageMath
4. Concept map table (Module concept -> Protocol application)
5. Summary

## Testing Your Changes

```bash
# Rust: everything should compile cleanly
cargo build --workspace

# Notebooks: open in SageMath and run all cells
conda activate sage
sage -n jupyter
```

## Pull Requests

- One module per PR when possible
- Describe what you changed and why
- If adding a notebook, mention which README section it fulfills
- Run all code cells before submitting

## Code of Conduct

Be kind, be patient, be helpful. These materials are for learners at all levels.
