from app.application import bcrypt


def encrypt(plain):
    return bcrypt.generate_password_hash(plain)


def verify_password(plain, hashed):
    return bcrypt.check_password_hash(hashed, plain)

