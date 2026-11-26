"""The Funniest Excuse for Skipping a Meeting -- round 2.

Writes one line (1-200 characters, UTF-8, not only whitespace) to
/output/entry.txt, or to $ENTRY_OUTPUT when set.

The build keeps three brand-new candidate excuses, each written from a
different angle, and scores each one 0-5 against the judge's criteria, in
the judge's own order:

  1. a funny one-line excuse for skipping a pointless work meeting / Zoom
  2. a sharp, surprising twist that earns a laugh, not just a mild smile
  3. feels true to office life: the laugh comes with a nod of recognition
  4. one tight line, no wasted words or throat-clearing
  5. a fresh angle, not a stock excuse about bad wifi, a cat or a dentist

The winner is the candidate with the highest total; a tie is settled by
walking the criteria in order and taking the first difference. Nothing
here touches the network, the clock, or the filesystem beyond the single
output file, and nothing is random.

Round 1 scored ~39.9% and landed outside the prize zone, so every line
below is written from scratch: no lift, no calendar, no meeting with
oneself, and no recycled phrasing from the earlier entry.
"""

import os

# The judge's criteria, in the order the judge weighs them.
CRITERIA = (
    "on_topic",
    "twist",
    "relatable",
    "tight",
    "fresh",
)

# Words the judge explicitly calls stock excuses, plus the three angles
# round 1 already used up. No candidate may carry any of them; the gate
# below enforces this on the winner.
BANNED_WORDS = ("wifi", "cat", "dentist", "lift", "calendar")

# Each candidate carries its line, its per-criterion scores, and one short
# note per criterion explaining the score.
CANDIDATES = [
    {
        "text": (
            "Sorry, my smart speaker joined the meeting for me and is "
            "nodding along better than I ever could."
        ),
        "scores": {
            "on_topic": 5,
            "twist": 5,
            "relatable": 5,
            "tight": 4,
            "fresh": 5,
        },
        "notes": {
            # 1. A direct excuse for skipping this meeting, addressed to
            #    the people waiting in it.
            "on_topic": "direct excuse for skipping this meeting",
            # 2. The gadget does not just fail, it outperforms you at
            #    your own job: it joined, it nods, and it is better at
            #    being in the meeting than you are.
            "twist": "the device replaces me and does it better",
            # 3. Everyone has nodded along blankly through a pointless
            #    Zoom, and everyone has had a smart device act on its own.
            "relatable": "blank nodding in Zoom plus a device with a mind of its own",
            # 4. One sentence, no filler; only "better than I ever could"
            #    runs a touch long, which is why this is a 4, not a 5.
            "tight": "one sentence, only the closing clause runs long",
            # 5. A smart speaker hijacking the meeting is not a stock
            #    excuse and uses none of the banned angles.
            "fresh": "gadget hijack, no stock excuse anywhere in it",
        },
    },
    {
        "text": (
            "I've read the agenda three times and my name appears nowhere, "
            "so I'm respecting the document's wishes."
        ),
        "scores": {
            "on_topic": 5,
            "twist": 4,
            "relatable": 4,
            "tight": 5,
            "fresh": 5,
        },
        "notes": {
            # 1. A clear reason for not showing up to this meeting.
            "on_topic": "clear reason for not attending this meeting",
            # 2. The agenda is treated as an authority whose wishes must
            #    be obeyed; witty, but cleverness rather than a belly laugh.
            "twist": "the agenda itself excludes me, so I obey it",
            # 3. Agendas that never mention you are a real office
            #    experience, though reading one three times is specific.
            "relatable": "agendas that never mention you are real",
            # 4. Every word earns its place; the punch lands in the last
            #    four words.
            "tight": "no wasted words, punch in the last clause",
            # 5. Letting a document decide your attendance is a new angle.
            "fresh": "document-as-boss angle, not a stock excuse",
        },
    },
    {
        "text": (
            "I was trying to look busy when I accidentally declined, and "
            "frankly the decline contributed more than I would have."
        ),
        "scores": {
            "on_topic": 5,
            "twist": 4,
            "relatable": 5,
            "tight": 4,
            "fresh": 4,
        },
        "notes": {
            # 1. A straightforward excuse for missing the meeting.
            "on_topic": "straightforward excuse for missing the meeting",
            # 2. The accidental decline outperforms attendance: a good
            #    second punch, but the accidental-decline joke is a known
            #    shape.
            "twist": "the decline did more work than attending would",
            # 3. Performing busyness and fat-fingering a button are both
            #    everyday office behaviour.
            "relatable": "performing busyness and fat-fingering a button",
            # 4. Runs a little long; "frankly" and "trying to look busy"
            #    could be trimmed.
            "tight": "a little long, could be trimmed",
            # 5. Self-sabotage is a fresh-ish angle, but the accidental
            #    decline has been joked about before.
            "fresh": "self-sabotage angle, partly familiar shape",
        },
    },
]


def score_key(candidate):
    """Sort key: total first, then each criterion in the judge's order."""
    scores = candidate["scores"]
    return (sum(scores[name] for name in CRITERIA),) + tuple(
        scores[name] for name in CRITERIA
    )


def pick_winner(candidates):
    """Deterministic pick: the candidate with the best score key."""
    return max(candidates, key=score_key)["text"]


def gate(line):
    """The entry must pass every rule the sealed scorer enforces, plus
    our own ban on stock and already-used angles."""
    assert isinstance(line, str), "winner must be text"
    assert 1 <= len(line) <= 200, "winner must be 1-200 characters"
    assert "\n" not in line and "\r" not in line, "winner must be one line"
    assert line == line.strip(), "winner must have no edge whitespace"
    assert line.strip(), "winner must not be only whitespace"
    assert "  " not in line, "winner must not contain double spaces"
    words = set(line.lower().replace(".", "").replace(",", "").split())
    for banned in BANNED_WORDS:
        assert banned not in words, f"winner uses banned word: {banned}"


def main():
    winner = pick_winner(CANDIDATES)
    gate(winner)

    out_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(winner)


if __name__ == "__main__":
    main()
