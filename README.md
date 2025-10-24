# DESAFIOS

Small repository of programming challenges (desafios) with solutions, tests and notes.

## Repository structure
- /challenges
    - /<challenge-name>
        - README.md — problem statement
        - solution.<ext> — reference solution
        - tests/ — unit tests or example inputs
- /docs — optional notes or explanations
- README.md — this file

## Purpose
Collect, solve and document short algorithmic or implementation challenges for practice, review and interview preparation.

## Getting started
1. Clone:
     git clone <repo-url>
2. Enter a challenge:
     cd challenges/<challenge-name>
3. Run tests (example):
     - Node: npm install && npm test
     - Python: python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt && pytest

Adjust commands to the language/runtime used in each challenge.

## Adding a challenge
1. Create a new folder under `challenges/` with a short, kebab-case name.
2. Add `README.md` with: problem description, constraints, examples.
3. Add `solution.<ext>` and a `tests/` folder with reproducible tests.
4. Optionally add a short explanation or complexity analysis.

## Contributing
- Open an issue for new challenge ideas or corrections.
- Submit PRs with a clear problem statement and passing tests.
- Keep solutions well-documented and tested.

## License
MIT — see LICENSE file for details.

## Contact
Open issues or pull requests on the repository.
