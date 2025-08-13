# Use Cases

Each use case must be implemented in its own file inside the `use_cases` directory.
Example:
`create_user.py`
`update_user.py`
`delete_user.py`

A use case file should contain only the logic for that specific business action.
It must not mix unrelated behaviors.

Each use case should declare its own DTO (Data Transfer Object) inside the same file.
The DTO defines the structure and types of the input and output data for that use case.

Guidelines:

- One file per use case.
- DTOs are local to the use case and defined alongside it.
- Avoid sharing DTOs between unrelated use cases.
- Keep DTOs immutable where possible.
