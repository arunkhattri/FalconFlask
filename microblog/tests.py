from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post
from hashlib import md5


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='maira')
        u.set_password('mia')
        self.assertFalse(u.check_password('cat'))
        self.assertTrue(u.check_password('mia'))

    def test_avatar(self):
        email = 'booboo@example.com'
        url = 'https://www.gravatar.com/avatar/'
        u = User(username='booboo', email=email)
        digest = md5(email.lower().encode('utf-8')).hexdigest()
        gravatar = '{}{}?d=identicon&s={}'.format(url, digest, 128)
        self.assertEqual(u.avatar(128), gravatar)

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='minoo', email='minoo@example.com')
        u2 = User(username='booboo', email='booboo@example.com')
        u3 = User(username='inoo', email='inoo@example.com')
        u4 = User(username='mia', email='mia@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from minoo", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from booboo", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from inoo", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from mia", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # minoo follows booboo
        u1.follow(u4)  # minoo follows mia
        u2.follow(u3)  # booboo follows inoo
        u3.follow(u4)  # mary follows mia
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == "__main__":
    unittest.main(verbosity=2)
