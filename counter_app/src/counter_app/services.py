from sqlalchemy.orm import Session

from counter_app.models import Counter


def get_or_create_counter(db_sess: Session) -> Counter:
    """Retrieve the counter from the db or create it if it doesn't exist."""
    counter = db_sess.query(Counter).first()

    if counter is None:
        counter = Counter(value=0)
        db_sess.add(counter)
        db_sess.commit()
        db_sess.refresh(counter)

    return counter


def modify_counter_by_value(db_sess: Session, amount: int) -> Counter:
    """Modify the counters value by the specified amount."""
    counter = get_or_create_counter(db_sess)
    counter.value += amount
    db_sess.commit()
    db_sess.refresh(counter)

    return counter


def set_counter_to_value(db_sess: Session, value: int) -> Counter:
    """Set the counter to the specified value."""
    counter = get_or_create_counter(db_sess)
    counter.value = value
    db_sess.commit()
    db_sess.refresh(counter)

    return counter
