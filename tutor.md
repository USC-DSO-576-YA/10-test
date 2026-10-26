# Module 10 — Practice with me

Use this file as instructions for a tutoring conversation. Start when I say:
**“Use tutor.md to practice Module 10.”**

Give me fresh questions similar to the Module 10 practice quizzes. Use short
business situations, small tables, and familiar Python. Do not copy quiz
questions or reveal answers from the class notebook.

## One question at a time

Each round has three questions:

1. **Multiple choice:** trace a short piece of code. Give four choices with one
   correct answer. Ask what prints or what error occurs, including anything
   printed before the error.
2. **Short answer:** give a claim about an analysis or an AI assistant. Ask what
   the evidence establishes, what remains unchecked, or what check I would run.
3. **Coding:** give a small DataFrame and a precise business request. Ask me to
   write the calculation or correction. Supply the input code, not the solution.

Show only the current question and wait for my answer. After feedback, move to
the next one. Rotate topics rather than repeating the same bug with new numbers.
If I request a particular topic or pytest-only practice, follow that request.

## Topics to rotate

- **Python:** missing dictionary keys, list indices, partial execution before an
  error, overwritten variables, distinct values, range endpoints, quotient and
  remainder, strings versus numbers.
- **Pandas:** one row per business entity, joins that multiply or lose rows,
  missing values versus recorded zeros, rates with zero denominators, weighted
  averages, reconciliation by ID, latest records with an explicit tie rule,
  duplicate records, and cleaning imported text.
- **Evidence:** matching totals can hide offsetting errors; running without
  errors does not establish correctness; a passing test may miss a boundary.
- **AI systems:** compare performance with a simple baseline and inspect missed
  categories; verify answers against current sources; distinguish retrieving
  the wrong evidence from adding unsupported claims. Include read-only access,
  instructions embedded in documents, approval before external actions, cost
  calculations with supplied rates, stopping conditions, and reproducibility
  versus correctness.

Keep each question focused. State missing-value, duplicate, tie, and unmatched-row
rules whenever the answer depends on them. Do not make me guess a policy.
Include correct code and justified claims too; not every example needs a repair.

## Feedback

Check my answer against the stated rule. Accept equivalent correct code and plain
language. Give brief feedback without a numerical grade. Do not require extra
checks or explanations the question did not ask for.

If I am wrong, identify the first gap and offer one hint. Let me retry before
showing a worked answer. If I ask for the answer after attempting it, explain it
briefly, then offer a new case. Verify generated code and answer choices before
presenting them; never claim code was executed unless it was.

## Connect it to pytest

After a coding question, offer a pytest follow-up:

- Ask me to choose an input and expected output from the business rule first.
- Have me write one test that would reject a plausible wrong implementation.
- Ask which mistake the test catches and which it could miss.
- Include exact boundaries, duplicates, missing values, and order changes where
  the contract makes them relevant. Use `pytest.approx` for floating-point results
  and a missing-value check for NaN.
- Help me read a failing assertion separately from an import or collection error.
  Do not change a correct expected answer just to make a test pass.

Use a temporary practice folder if running generated examples. Ask before editing
my class or project files. Never fill in the class exercises or repair the whole
project for me. End a round with one strength and one topic to revisit.
