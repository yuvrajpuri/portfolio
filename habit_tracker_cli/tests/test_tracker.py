import json
import tracker
import pytest


@pytest.fixture
def isolated_tracker(tmp_path, monkeypatch):
    test_file = tmp_path / "data.json"
    monkeypatch.setattr(tracker, "DATA_FILE", str(test_file))
    return test_file


def test_create_habit(isolated_tracker):

    tracker.create_habit("Gundam")

    with open(isolated_tracker) as f:
        data = json.load(f)

    assert "Gundam" in data["habit"]


def test_duplicate_habit(isolated_tracker):

    tracker.create_habit("Gundam")
    tracker.create_habit("Gundam")

    data = tracker.get_habits()

    assert len(data["habit"]) == 1


def test_log_update(isolated_tracker):

    tracker.create_habit("Coding")
    tracker.update_tracker("Coding")

    data = tracker.get_habits()

    logs = data["habit"]["Coding"]["logs"]

    assert len(logs) == 1


def test_metadata_update(isolated_tracker):

    tracker.create_habit("Workout")

    tracker.update_tracker("Workout", mood="great")

    data = tracker.get_habits()

    metadata = data["habit"]["Workout"]["metadata"]

    assert "mood" in metadata
    assert metadata["mood"][0] == "great"


def test_streak_basic():

    tracker_data = {
        "habit": {
            "Test": {
                "logs": [],
                "metadata": {}
            }
        }
    }

    streak = tracker.return_streak("Test", tracker_data)

    assert streak == 0


def test_streak_three_entries():

    tracker_data = {
        "habit": {
            "Test": {
                "logs": [
                    "2026-01-01T10:00:00+00:00",
                    "2026-01-01T15:00:00+00:00",
                    "2026-01-01T20:00:00+00:00"
                ],
                "metadata": {}
            }
        }
    }

    streak = tracker.return_streak("Test", tracker_data)

    assert streak == 3


def test_update_missing_habit(isolated_tracker):

    tracker.create_habit("Reading")

    tracker.update_tracker("FakeHabit")

    data = tracker.get_habits()

    assert "Reading" in data["habit"]