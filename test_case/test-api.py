# Trong file tests/test_api.py
import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db  # Import Flask app và database từ file app.py
from db.models import Student
class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Khởi tạo Flask app context
        cls.app = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()

        # Thiết lập cấu hình cho Flask để sử dụng cơ sở dữ liệu tạm thời
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        # Tạo database schema
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Xóa cơ sở dữ liệu và loại bỏ Flask app context
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        # Tạo dữ liệu mẫu
        student1 = Student(full_name='John Doe', gender='Male', school='ABC University')
        student2 = Student(full_name='Jane Smith', gender='Female', school='XYZ College')
        db.session.add(student1)
        db.session.add(student2)
        db.session.commit()

    def tearDown(self):
        # Xóa dữ liệu sau mỗi test case
        db.session.query(Student).delete()
        db.session.commit()

    def test_list_students(self):
        # Gọi API
        response = self.app.get('/api/students')
        data = response.get_json()

        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['full_name'], 'John Doe')
        self.assertEqual(data[1]['gender'], 'Female')

    def test_get_student(self):
        # Gọi API
        response = self.app.get('/api/student/1')
        data = response.get_json()

        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['school'], 'ABC University')

    def test_create_student(self):
        # Gọi API
        response = self.app.post('/api/student', json={'full_name': 'John Doe', 'gender': 'Male', 'school': 'ABC University'})

        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Student.query.count(), 3)  # 2 từ setUp + 1 từ test case này

    def test_update_student(self):
        # Gọi API
        response = self.app.put('/api/student/1', json={'school': 'XYZ College'})

        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.query.get(1).school, 'XYZ College')

    def test_delete_student(self):
        # Gọi API
        response = self.app.delete('/api/student/1')

        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Student.query.count(), 1)

if __name__ == '__main__':
    unittest.main()
