import pytest
import sqlite3
from boxing.models.boxers_model import (
    create_boxer,
    delete_boxer,
    get_boxer_by_id,
    get_boxer_by_name,
    get_leaderboard,
    get_weight_class,
    update_boxer_stats,
    Boxer
)

@pytest.fixture()
def test_db(tmp_path):
    """Fixture to create a temporary SQLite database for boxing tests."""
    db_path = tmp_path / "test_boxing.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    # Create table similar to production schema.
    cursor.execute("""
        CREATE TABLE boxers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            weight INTEGER,
            height INTEGER,
            reach REAL,
            age INTEGER,
            fights INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    yield conn
    conn.close()

@pytest.fixture
def monkeypatch_db(monkeypatch, test_db):
    """Patch get_db_connection to use the test database."""
    from boxing.models.boxers_model import get_db_connection
    monkeypatch.setattr("boxing.models.boxers_model.get_db_connection", lambda: test_db)
    return test_db

@pytest.fixture
def sample_boxer():
    """Fixture providing a sample boxer dictionary."""
    return {"name": "Test Boxer", "weight": 150, "height": 175, "reach": 70.0, "age": 25}

def test_create_boxer_success(monkeypatch_db, sample_boxer):
    """Test creating a boxer successfully."""
    create_boxer(**sample_boxer)
    cursor = monkeypatch_db.cursor()
    cursor.execute("SELECT name FROM boxers WHERE name = ?", (sample_boxer["name"],))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == sample_boxer["name"]

def test_create_boxer_invalid_weight(monkeypatch_db, sample_boxer):
    """Test that a boxer with invalid weight raises ValueError."""
    sample_boxer["weight"] = 120  # Invalid weight, below 125
    with pytest.raises(ValueError, match="Invalid weight: 120"):
        create_boxer(**sample_boxer)

def test_create_boxer_duplicate(monkeypatch_db, sample_boxer):
    """Test that attempting to create a duplicate boxer raises ValueError."""
    create_boxer(**sample_boxer)
    with pytest.raises(ValueError, match="Boxer with name 'Test Boxer' already exists"):
        create_boxer(**sample_boxer)

def test_delete_boxer(monkeypatch_db, sample_boxer):
    """Test deleting an existing boxer."""
    create_boxer(**sample_boxer)
    cursor = monkeypatch_db.cursor()
    cursor.execute("SELECT id FROM boxers WHERE name = ?", (sample_boxer["name"],))
    boxer_id = cursor.fetchone()[0]
    delete_boxer(boxer_id)
    cursor.execute("SELECT id FROM boxers WHERE id = ?", (boxer_id,))
    assert cursor.fetchone() is None

def test_get_boxer_by_id(monkeypatch_db, sample_boxer):
    """Test retrieving a boxer by ID."""
    create_boxer(**sample_boxer)
    cursor = monkeypatch_db.cursor()
    cursor.execute("SELECT id FROM boxers WHERE name = ?", (sample_boxer["name"],))
    boxer_id = cursor.fetchone()[0]
    boxer = get_boxer_by_id(boxer_id)
    assert boxer.id == boxer_id
    assert boxer.name == sample_boxer["name"]

def test_get_boxer_by_name(monkeypatch_db, sample_boxer):
    """Test retrieving a boxer by name."""
    create_boxer(**sample_boxer)
    boxer = get_boxer_by_name(sample_boxer["name"])
    assert boxer.name == sample_boxer["name"]

def test_get_weight_class():
    """Test get_weight_class returns the correct class for given weights."""
    assert get_weight_class(205) == 'HEAVYWEIGHT'
    assert get_weight_class(170) == 'MIDDLEWEIGHT'
    assert get_weight_class(135) == 'LIGHTWEIGHT'
    assert get_weight_class(130) == 'FEATHERWEIGHT'
    with pytest.raises(ValueError, match="Invalid weight: 120"):
        get_weight_class(120)

def test_update_boxer_stats(monkeypatch_db, sample_boxer):
    """Test updating boxer stats for win and loss."""
    create_boxer(**sample_boxer)
    cursor = monkeypatch_db.cursor()
    cursor.execute("SELECT id, fights, wins FROM boxers WHERE name = ?", (sample_boxer["name"],))
    row = cursor.fetchone()
    boxer_id, fights_before, wins_before = row

    update_boxer_stats(boxer_id, "win")
    cursor.execute("SELECT fights, wins FROM boxers WHERE id = ?", (boxer_id,))
    fights_after, wins_after = cursor.fetchone()
    assert fights_after == fights_before + 1
    assert wins_after == wins_before + 1

    update_boxer_stats(boxer_id, "loss")
    cursor.execute("SELECT fights, wins FROM boxers WHERE id = ?", (boxer_id,))
    fights_final, wins_final = cursor.fetchone()
    assert fights_final == fights_after + 1
    assert wins_final == wins_after

def test_get_leaderboard(monkeypatch_db, sample_boxer):
    """Test that the leaderboard is correctly generated and sorted by wins."""
    # Create two boxers with different stats.
    create_boxer(**sample_boxer)
    boxer1 = get_boxer_by_name(sample_boxer["name"])
    sample_boxer2 = sample_boxer.copy()
    sample_boxer2["name"] = "Second Boxer"
    sample_boxer2["weight"] = 160
    sample_boxer2["height"] = 180
    sample_boxer2["reach"] = 68.0
    sample_boxer2["age"] = 30
    create_boxer(**sample_boxer2)
    boxer2 = get_boxer_by_name(sample_boxer2["name"])

    # Update stats: mark boxer1 as win and boxer2 as loss.
    update_boxer_stats(boxer1.id, "win")
    update_boxer_stats(boxer2.id, "loss")

    leaderboard = get_leaderboard("wins")
    # Expect boxer1 to rank higher because he has a win.
    assert leaderboard[0]["id"] == boxer1.id
