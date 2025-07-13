from rest_framework.test import APITestCase
from lms.models import Lesson, CourseSubscription, Course
from users.models import User


class LessonsTestCase(APITestCase):
    """
    Test case for the Lessons API.
    """

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(
            name="Lesson",
            description="This is a test lesson.",
            owner=self.user
        )

    def test_lesson_create(self):
        """
        Test creating a lesson.
        """
        data = {
            "name": "Test Lesson",
            "description": "This is a test lesson.",

        }
        response = self.client.post('/lessons/create/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Lesson.objects.filter(name="Test Lesson").exists())

    def test_lesson_list(self):
        """
        Test listing all lessons.
        """
        response = self.client.get('/lessons/')
        data = response.json()
        result = data.get("results", [])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]["name"], "Lesson")

    def test_lesson_detail(self):
        """
        Test retrieving a lesson detail.
        """
        response = self.client.get(f'/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Lesson")
        self.assertEqual(data["description"], "This is a test lesson.")

    def test_lesson_update(self):
        """
        Test updating a lesson.
        """
        data = {
            "name": "Updated Lesson",
            "description": "This is an updated test lesson.",
        }
        response = self.client.put(f'/lessons/{self.lesson.id}/update/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Updated Lesson")
        self.assertEqual(self.lesson.description, "This is an updated test lesson.")

    def test_lesson_delete(self):
        """
        Test deleting a lesson.
        """
        response = self.client.delete(f'/lessons/{self.lesson.id}/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class CourseSubscriptionTestCase(APITestCase):
    """
    Test case for the Lessons API.
    """

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Test Course",
            description="This is a test course.",
            owner=self.user
        )

    def test_course_subscription_create(self):
        """
        Test creating a course subscription.
        """
        data = {
            "course": self.course.id
        }
        response = self.client.post('/subscriptions/', data, format='json')
        data = CourseSubscription.objects.filter(course=self.course)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(CourseSubscription.objects.filter(user=self.user).exists())
        self.assertEqual(data[0].user, self.user)

    def test_course_subscription_delete(self):
        """
        Test deleting a course subscription.
        """
        data = {"course": self.course.id}

        # First call: create
        response_create = self.client.post('/subscriptions/', data, format='json')
        self.assertEqual(response_create.status_code, 201)
        self.assertTrue(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

        # Second call: delete
        response_delete = self.client.post('/subscriptions/', data, format='json')
        self.assertEqual(response_delete.status_code, 204)
        self.assertFalse(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())
