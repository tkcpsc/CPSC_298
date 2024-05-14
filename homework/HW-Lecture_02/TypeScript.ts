interface Email {
  value: string;
}

interface SecureString {
  value: string;
}

interface HashedPassword {
  algorithm: string;
  hash: string;
}

interface User {
  username: Email;
  hashedPassword: HashedPassword;
}

interface LoginCredentials {
  username: Email;
  password: SecureString;
}

function validateEmail(email: string): Email | null {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email) ? { value: email } : null;
}

function hashPassword(password: SecureString): HashedPassword {
  const salt = "your_salt_here"; // Securely generate and store salt
  const hash = `hashed_${password.value}_${salt}`; // Simulate hashing
  return { algorithm: "SHA-256", hash: hash };
}

// Mock database of users
const users: User[] = [
  {
    username: { value: "example@example.com" },
    hashedPassword: {
      algorithm: "SHA-256",
      hash: "hashed_securePassword123!_your_salt_here"
    }
  }
];

function getUserByUsername(username: string): User | undefined {
  return users.find(user => user.username.value === username);
}

function login(credentials: LoginCredentials): boolean {
  const userFromDB: User | undefined = getUserByUsername(credentials.username.value);
  if (!userFromDB) {
    return false; // User not found
  }
  const hashedPassword = hashPassword(credentials.password);

  return userFromDB.hashedPassword.hash === hashedPassword.hash;
}

// Example usage
const userCredentials = {
  username: validateEmail("example@example.com")!,
  password: { value: "securePassword123!" }
};

const isAuthenticated = login(userCredentials);
console.log(`Is authenticated: ${isAuthenticated}`);
