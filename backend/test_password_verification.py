from passlib.context import CryptContext

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Example hashed password from the database
hashed_password = "$2b$12$qYjmBcN8rf7BPsvK4A1KtOy7QXgp9WKHqfqo2BcFa0AP7T1b4mrEe"
# Password to verify
password_to_test = "your_password_here"  # Replace with the actual password

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Test the password
if verify_password(password_to_test, hashed_password):
    print("Password is valid!")
else:
    print("Invalid password.")
