import pytest
from department import Department, CONN, CURSOR

@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown():
    """Setup and teardown for tests."""
    Department.create_table()
    yield
    Department.drop_table()

def test_creates_table():
    """Tests if the table is created correctly."""
    Department.create_table()
    result = CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='departments'").fetchone()
    assert result is not None

def test_drops_table():
    """Tests if the table is dropped correctly."""
    Department.create_table()  # Ensure the table exists before dropping it
    Department.drop_table()
    result = CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='departments'").fetchone()
    assert result is None

def test_saves_department():
    """Tests if a department is saved correctly."""
    department = Department("Payroll", "Building A, 5th Floor")
    department.save()
    row = CURSOR.execute("SELECT * FROM departments").fetchone()
    assert row is not None
    assert row[1] == "Payroll"
    assert row[2] == "Building A, 5th Floor"

def test_creates_department():
    """Tests if a department is created correctly using class method."""
    department = Department.create("Payroll", "Building A, 5th Floor")
    row = CURSOR.execute("SELECT * FROM departments WHERE id = ?", (department.id,)).fetchone()
    assert row is not None
    assert row[1] == "Payroll"
    assert row[2] == "Building A, 5th Floor"

def test_updates_row():
    """Tests if a department's details are updated correctly."""
    department1 = Department.create("Human Resources", "Building C, East Wing")
    department2 = Department.create("Marketing", "Building B, 3rd Floor")
    department2.name = "Sales and Marketing"
    department2.location = "Building B, 4th Floor"
    department2.update()
    row = CURSOR.execute("SELECT * FROM departments WHERE id = ?", (department2.id,)).fetchone()
    assert row[1] == "Sales and Marketing"
    assert row[2] == "Building B, 4th Floor"

def test_deletes_record():
    """Tests if a department record is deleted correctly."""
    department1 = Department.create("Human Resources", "Building C, East Wing")
    department1_id = department1.id
    department2 = Department.create("Marketing", "Building B, 3rd Floor")
    department2.delete()
    row = CURSOR.execute("SELECT * FROM departments WHERE id = ?", (department1_id,)).fetchone()
    assert row is not None
    row = CURSOR.execute("SELECT * FROM departments WHERE id = ?", (department2.id,)).fetchone()
    assert row is None
