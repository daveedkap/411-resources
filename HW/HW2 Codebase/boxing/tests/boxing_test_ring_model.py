import math
import pytest
from boxing.models.ring_model import RingModel
from boxing.models.boxers_model import Boxer

@pytest.fixture
def ring_model():
    """Fixture to provide a new instance of RingModel for each test."""
    return RingModel()

@pytest.fixture
def sample_boxer1():
    """Fixture providing a sample Boxer instance."""
    return Boxer(id=1, name="Boxer One", weight=150, height=170, reach=70.0, age=25)

@pytest.fixture
def sample_boxer2():
    """Fixture providing a second sample Boxer instance."""
    return Boxer(id=2, name="Boxer Two", weight=160, height=175, reach=72.0, age=30)

##################################################
# Ring Management Tests
##################################################

def test_enter_ring_success(ring_model, sample_boxer1):
    """Test that a boxer can successfully enter the ring."""
    ring_model.enter_ring(sample_boxer1)
    boxers = ring_model.get_boxers()
    assert len(boxers) == 1, "Expected ring to have 1 boxer after entry"
    assert boxers[0] == sample_boxer1, "The boxer in the ring should be sample_boxer1"

def test_enter_ring_full(ring_model, sample_boxer1, sample_boxer2):
    """Test that entering a boxer into a full ring raises an error."""
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    with pytest.raises(ValueError, match="Ring is full, cannot add more boxers."):
        ring_model.enter_ring(sample_boxer1)

def test_clear_ring(ring_model, sample_boxer1, sample_boxer2):
    """Test that clearing the ring empties it."""
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    ring_model.clear_ring()
    assert len(ring_model.get_boxers()) == 0, "Expected ring to be empty after clearing"

def test_get_boxers(ring_model, sample_boxer1):
    """Test that get_boxers returns the current list of boxers in the ring."""
    ring_model.enter_ring(sample_boxer1)
    boxers = ring_model.get_boxers()
    assert boxers == [sample_boxer1], "Expected get_boxers to return a list with sample_boxer1"

##################################################
# Fighting Skill and Fight Tests
##################################################

def test_get_fighting_skill(ring_model, sample_boxer1):
    """Test calculating the fighting skill for a boxer."""
    # Calculation: skill = (weight * len(name)) + (reach/10) + age_modifier
    # For sample_boxer1: age=25 yields age_modifier=0
    expected_skill = (sample_boxer1.weight * len(sample_boxer1.name)) + (sample_boxer1.reach / 10) + 0
    actual_skill = ring_model.get_fighting_skill(sample_boxer1)
    assert math.isclose(actual_skill, expected_skill, rel_tol=1e-5), "Fighting skill calculation is incorrect."

def test_fight_insufficient_boxers(ring_model, sample_boxer1):
    """Test that a fight cannot start with fewer than 2 boxers."""
    ring_model.enter_ring(sample_boxer1)
    with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
        ring_model.fight()

def test_fight_success(ring_model, sample_boxer1, sample_boxer2, monkeypatch):
    """Test that a fight completes successfully and the ring is cleared afterwards."""
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    
    # Patch get_random to return 0.0 so that the logic chooses boxer1 as winner.
    monkeypatch.setattr("boxing.models.ring_model.get_random", lambda: 0.0)
    # Patch update_boxer_stats to be a no-op.
    monkeypatch.setattr("boxing.models.ring_model.update_boxer_stats", lambda boxer_id, result: None)
    
    winner_name = ring_model.fight()
    assert winner_name == sample_boxer1.name, "Expected the winner to be sample_boxer1 based on patched random number."
    assert len(ring_model.get_boxers()) == 0, "Expected the ring to be cleared after the fight."
