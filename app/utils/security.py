

def encrypt(plain):
    from app.application import bcrypt
    return bcrypt.generate_password_hash(plain)


def verify_password(plain, hashed):
    from app.application import bcrypt
    return bcrypt.check_password_hash(hashed, plain)

