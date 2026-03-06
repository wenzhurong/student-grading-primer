# Edge Case Chosen

## Edge case
`POST /students` allows `mark` to be optional in the primer spec. This creates ambiguity for stats calculation when mark is missing.

## Decision
If `mark` is not provided, I store it as `0`.

## Why
- It keeps every stored student record consistent (`mark` is always an integer).
- It avoids special-case handling for `None` marks in update and stats logic.
- It keeps API behavior predictable and easy to explain/test.

## Where this is implemented
In `backend/app.py` inside `create_student()`, `mark` is read as:

`mark = student_data.get("mark", 0)`

and then validated to be an integer between `0` and `100`.
