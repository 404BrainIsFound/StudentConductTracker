A simple student conduct tracker using flask

# Commands
Added app command `demo` (usage "flask demo") which creates a few Student and Review records in order to demonstrate functionality.

Added command groups `staff` and `admin` to simulate the different operations these roles may perform.

# Staff Commands
`add-review`
Displays all student records and prompts for a student ID to add a review for.

`search-student-id {id}` and `search-student-name {name}`
Accepts an ID or name and searches Student records for a direct match.

`view-reviews {id}`
Displays all reviews for a student with a particular student ID.

# Admin Commands
`add-student {id} {name} {degree | "None"} {department | "None"} {faculty | "None"}`
Creates a new student record with the given information.
