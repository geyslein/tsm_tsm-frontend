import base64
import hashlib
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.utils.crypto import pbkdf2


class MosquittoGoAuthPBKDF2SHA512PasswordHasher(PBKDF2PasswordHasher):
    """
    From https://gist.github.com/simonwhitaker/4474381

    Alternate PBKDF2 hasher which uses SHA512 instead of SHA256.

    Note: As of Django 1.4.3, django.contrib.auth.models.User defines password
    with max_length=128

    Our superclass (PBKDF2PasswordHasher) generates the entry for that field
    using the following format (see
    https://github.com/django/django/blob/1.4.3/django/contrib/auth/hashers.py#L187):

        "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    The lengths of the various bits in that format are:

     13  self.algorithm ("pbkdf2_sha512")
      5  iterations ("10000" - inherited from superclass)
     12  salt (generated using django.utils.crypto.get_random_string())
     89  hash (see below)
      3  length of the three '$' separators
    ---
    122  TOTAL

    122 <= 128, so we're all good.

    NOTES

    hash is the base-64 encoded output of django.utils.crypto.pbkdf2(password, salt,
    iterations, digest=hashlib.sha512), which is 89 characters according to my tests.

        >>> import hashlib
        >>> from django.utils.crypto import pbkdf2
        >>> len(pbkdf2('t0ps3kr1t', 'saltsaltsalt', 10000, 0, hashlib.sha512).encode('base64').strip())
        89

    It's feasible that future versions of Django will increase the number of iterations
    (but we only lose one character per power-of-ten increase), or the salt length. That
    will cause problems if it leads to a password string longer than 128 characters, but
    let's worry about that when it happens.
    """
    algorithm = "PBKDF2"
    digest = hashlib.sha512
    digest_name = digest.__name__.split('openssl_')[-1]

    def encode(self, password, salt, iterations=None):
        self._check_encode_args(password, salt)
        iterations = iterations or self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode("ascii").strip()
        # return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)
        return "%s$%s$%d$%s$%s" % (
            self.algorithm,
            self.digest_name,
            iterations,
            base64.b64encode(salt.encode("ascii")).decode("ascii").strip(),
            hash
        )

    def decode(self, encoded):
        algorithm, digest, iterations, salt, hash = encoded.split("$", 4)
        assert algorithm == self.algorithm
        assert digest == self.digest_name
        return {
            "algorithm": algorithm,
            "hash": hash,
            "iterations": int(iterations),
            "salt": base64.b64decode(salt).decode("ascii"),
        }
