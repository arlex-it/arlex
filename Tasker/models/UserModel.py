"""
User modelization.
"""

import hashlib
import arrow
from arrow.parser import ParserError
from dateutil.relativedelta import relativedelta
from mongoengine import StringField

from Tasker.helpers.PasswordHelper import PasswordHelper
from Tasker.helpers.exceptions import ModelError
from Tasker.helpers.generic import load_config
from Tasker.models.AbstractModel import AbstractModel

config = load_config()

DEFAULT_KMS_NUMBER = 25

class UserModel(AbstractModel):
    """
    User model.
    """

    meta = {'collection': 'users'}
    id = StringField(primary_key=True)

    @property
    def all_emails(self):
        return self.get('emails')


    @property
    def address(self):
        """
        ? Return the first address in profile ?

        :rtype: ? or None
        """
        if 'profile' not in self or self.profile is None:
            return None

        if 'addresses' not in self.profile or self.profile['addresses'] is None:
            return None

        for addr in self.profile['addresses']:
            if addr['name_address'] == 'home':
                return addr

        return self.profile['addresses'][0]

    @property
    def lastname(self):
        """
        :rtype: str
        """
        if self.get('profile.lastname') is not None:
            return self.get('profile.lastname')

        return ''

    @property
    def firstname(self):
        """
        :rtype: str
        """
        if self.get('profile.firstname') is not None:
            return self.get('profile.firstname')

        return ''

    @property
    def nickname(self):
        """
        :rtype: str
        """
        if self.get('profile') is None:
            return ''

        if self.get('profile.nickname') is not None:
            return self.get('profile.nickname')
        elif self.get('profile.firstname') is not None and self.get('profile.lastname') is not None:
            return '{} {}.'.format(
                self.get('profile.firstname'), self.get('profile.lastname')[0]
            )

        return ''

    @property
    def password(self):
        """
        Get hashed password.

        :rtype: str
        """
        return self.get('services.password.bcrypt')

    @property
    def age(self):
        """
        :return: The age of an user
        :rtype: int
        """
        try:
            birth_date = arrow.get(self.get('profile.birthdate')).datetime.date()
            return relativedelta(arrow.now().datetime.date(), birth_date).years
        except ParserError as exc:
            return None

    @property
    def role(self):
        """
        Get role.

        :rtype: str
        """
        return self.get('profile.role', default='')

    def create(self, firstname, lastname, phone, email):
        super(UserModel, self).create()

        self.hashes = []
        self.profile = {}
        self.services = {}
        self.status = {}
        self.notifs = {}
        self.username = email
        self.update_firstname(firstname)
        self.update_lastname(lastname)
        self.add_email(email)
        return self

    def is_admin(self):
        return self.role in ['admin', 'superadmin']

    def is_enabled(self):
        """
        :rtype: bool
        """
        if not self.get('profile.frozen') and not self.get('profile.toDelete'):
            return True

        return False

    def update_firstname(self, firstname):
        if not hasattr(self, 'profile'):
            self.profile = {}

        if self.is_field_locked('firstname'):
            raise ModelError('This field is locked')

        self.profile['firstname'] = firstname

    def update_lastname(self, lastname):
        if not hasattr(self, 'profile'):
            self.profile = {}

        if self.is_field_locked('lastname'):
            raise ModelError('This field is locked')

        self.profile['lastname'] = lastname

    def update_password(self, new_password):
        if not hasattr(self, 'services'):
            self.services = {}
        if not 'password' in self.services:
            self.services['password'] = {}

        hashed_password = PasswordHelper.hash_password(new_password)
        self.services['password']['bcrypt'] = hashed_password
        self.services = self.services  # yep, don't remove that !

    def add_email(self, email, verified=False):
        """
        Affect a new email address to the user.

        :param str email: new email address
        :param bool verified: does the email has been verified ?
        """
        if not hasattr(self, 'emails'):
            self.emails = []

        email = email.lower()
        if self.has_email(email):
            raise ModelError("Email already exists on this user")

        self.emails.append({'address': email, 'verified': verified})
        self._update_hashes()

    def has_email(self, email):
        """
        :rtype: bool
        """
        (exists, _) = self.__email_exists(email)
        return exists

    def _update_hashes(self):
        """
        Update local hash list of all emails and phone numbers.
        """
        if not hasattr(self, 'emails'):
            self.emails = []
        if not hasattr(self, 'phone'):
            self.phone = []

        hashes = []
        emails = [e['address'] for e in self.emails if 'address' in e]
        phones = [p['number'] for p in self.phone if 'number' in p]
        for elem in emails + phones:
            hashed_elem = hashlib.sha1(str(elem).encode('ascii', 'ignore')).hexdigest()
            hashes.append(hashed_elem)

        self.hashes = hashes

    def is_field_locked(self, field):
        if not hasattr(self, 'profile'):
            self.profile = {}

        if (
                'verifiedProfile' in self.profile
                and field in self.profile['verifiedProfile']
                and self.profile['verifiedProfile'][field]
        ):
            return True

        return False

    def __email_exists(self, searched_email):
        searched_email = searched_email.lower()

        if not hasattr(self, 'emails'):
            return False, -1

        for idx, email in enumerate(self.emails):
            if email['address'] == searched_email:
                return True, idx

        return False, -1