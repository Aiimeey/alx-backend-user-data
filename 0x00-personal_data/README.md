Project: Backend User Data Security

This project focuses on implementing secure handling and logging of personal data in a backend environment. It includes several modules and tasks aimed at ensuring data privacy and security principles are followed throughout the development process.
Modules and Tasks:

    Regex-ing (filter_datum function)
        Implements a function to obfuscate sensitive fields in log messages using regular expressions.

    Log Formatter (RedactingFormatter class)
        Custom log formatter that redacts specified fields from log messages using the filter_datum function.

    Create Logger (get_logger function)
        Sets up a logger (user_data) configured to log at INFO level with a StreamHandler using RedactingFormatter.

    Connect to Secure Database (get_db function)
        Connects to a MySQL database using credentials stored in environment variables, ensuring secure database access.

    Read and Filter Data (main function)
        Retrieves user data from the database and logs it in a filtered format using the user_data logger, ensuring sensitive fields are masked.

    Encrypting Passwords (hash_password function)
        Implements password hashing using bcrypt for secure storage of passwords.

    Check Valid Password (is_valid function)
        Validates passwords against their hashed versions using bcrypt, ensuring secure password verification.

Requirements and Usage:

    Each module and function adheres to specific coding standards (pycodestyle), documentation requirements, and security best practices.
    Environment variables (PERSONAL_DATA_DB_USERNAME, PERSONAL_DATA_DB_PASSWORD, PERSONAL_DATA_DB_HOST, PERSONAL_DATA_DB_NAME) are used to securely manage database credentials.
    The project includes comprehensive documentation in a README.md file explaining setup instructions, module descriptions, and usage guidelines.
