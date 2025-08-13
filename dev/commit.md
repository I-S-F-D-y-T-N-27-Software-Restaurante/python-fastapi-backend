# Commit Message Guidelines

---

## 1. Structure of a Commit Message

A commit message should have **three parts**:

```html

<type>(<scope>): <short summary> <BLANK LINE> <longer description if needed> <BLANK LINE>

<footer or references if needed>
```

* **type** – the category of the change
* **scope** – optional, the module or area affected
* **short summary** – ≤50 characters, imperative mood
* **longer description** – optional, wrap at 72 characters
* **footer** – optional, references to issues, breaking changes, etc.

---

## 2. Common Types

* `feat` – new feature
* `fix` – bug fix
* `docs` – documentation only changes
* `style` – formatting, whitespace, or code style
* `refactor` – code change that neither fixes a bug nor adds a feature
* `perf` – performance improvement
* `test` – adding or fixing tests
* `chore` – maintenance tasks, build process, tooling
* `ci` – continuous integration changes

---

## 3. Examples

```git
feat(auth): add JWT access token support

fix(database): handle connection timeout properly

docs(readme): update setup instructions

style(models): fix indentation and remove trailing whitespace

refactor(services): split user service into smaller functions
```

---

## 4. Best Practices

* **Use imperative mood**: “Add feature” instead of “Added feature”
* **Keep the summary short** (≤50 characters)
* **Separate subject from body with a blank line**
* **Use the body to explain why and how, not just what**
* **Reference issues or pull requests in the footer**: `Closes #42`
* **Do not include merge commits in the main history** unless necessary
* **Group related changes in a single commit**
* **Avoid committing generated files** or sensitive info

---

## 5. Example of a Full Commit

```git
feat(api): implement user registration endpoint

- Added POST /users endpoint for registration
- Validates input with Pydantic schema
- Saves new user to the database using SQLAlchemy
- Returns 201 and user info

Closes #12
```git

---

Following these guidelines ensures **clear history, easier code review, and better collaboration**.

```

This template follows **Conventional Commits**, which is widely used in professional projects and integrates well with changelog generation tools.
