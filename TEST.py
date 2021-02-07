import unittest
import os
from app import app, db, BackupData, Inspection, Auto, User, Owner


class TestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        result = self.app.get('/')

    def test_BackupData(self):
        b = BackupData(id=1, backupdate=234234555)
        db.session.add(b)
        db.session.commit()
        assert b.id == 1
        assert b.backupdate == 234234555

    def test_Inspection(self):
        i = Inspection(id=12221, date='01.01.2021', result='инспекция пройдена' , user_number=2, owner_number=3, auto_number=1)
        db.session.add(i)
        db.session.commit()
        assert i.id == 12221
        assert i.date == '01.01.2021'
        assert i.result == 'инспекция пройдена'
        assert i.user_number == 2
        assert i.owner_number == 3
        assert i.auto_number == 1


    def test_Auto(self):
        a = Auto(id=11, colour='красный', brand='Тайота', engine=112342,
                 technical_passport="Тайота Камри, АБ112,2021 года выпуска", inspection_id=1, owner_number=12)
        db.session.add(a)
        db.session.commit()
        assert a.id == 11
        assert a.colour == 'красный'
        assert a.brand == 'Тайота'
        assert a.engine == 112342
        assert a.technical_passport == "Тайота Камри, АБ112,2021 года выпуска"
        assert a.inspection_id == 1
        assert a.owner_number == 12

    def test_User(self):
        u = User(id=10, login='user123', password='qwerty12345',
                 officer_firstname='Иван',
                 officer_lastname='Иванов', officer_rank='Сержант', inspection_number='1')
        db.session.add(u)
        db.session.commit()
        assert u.id == 10
        assert u.login == 'user123'
        assert u.password == 'qwerty12345'
        assert u.officer_firstname == 'Иван'
        assert u.officer_lastname == 'Иванов'
        assert u.officer_rank == 'Сержант'

    def test_Owner(self):
        o = Owner(id='00100', adress='Россия,Архангельск,ул.Кутузова 6', gender='муж.', firstname='Виктор',
                  lastname='Иванов',
                  birthday='02.03.1970', license=112475758, auto_number= 11123 , inspection_number=8)
        db.session.add(o)
        db.session.commit()
        assert o.id == 100
        assert o.adress == 'Россия,Архангельск,ул.Кутузова 6'
        assert o.gender == 'муж.'
        assert o.firstname == 'Виктор'
        assert o.lastname == 'Иванов'
        assert o.birthday == '02.03.1970'
        assert o.license == 112475758
        assert o.auto_number== 11123
        assert o.inspection_number==8
if __name__ == '__main__':
    unittest.main()
