"""Selection: the part of the radar that decides what a reader sees.

Three passes, each answering a question the others structurally cannot:

- `gate`   per item, cheap. Could this matter at all, and to which theme?
- `rank`   listwise. Which of these matters most? The only stage that sees the set.
- `defend` per item, full read. Does this clear the bar on its own merits?

"Top N" is a property of a set, so it cannot be computed from independent
judgements of members. That is why ranking is a separate pass rather than a
better prompt on the per-item one.
"""

from .adapter import to_candidate, to_candidates
from .contract import Candidate, DefendVerdict, GateVerdict, SelectionResult
from .pipeline import SelectionSettings, select

# The individual passes stay behind their modules (`selection.gate`,
# `selection.rank`, `selection.defend`). Re-exporting a function named `rank`
# from a package that also contains a module named `rank` shadows the module,
# which is confusing to import and easy to get subtly wrong.
__all__ = [
    "Candidate",
    "GateVerdict",
    "DefendVerdict",
    "SelectionResult",
    "SelectionSettings",
    "to_candidate",
    "to_candidates",
    "select",
]
