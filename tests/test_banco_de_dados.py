from testcase import TestCase

from app import app


class AsserteTrue:
    pass


class MyTest(TestCase):

    db = "http://127.0.0.1:5000"
    da = 'http://192.168.1.2:5000'
    def test_case(self):

        results = {
            self.db: self._check_connectivity(self.db),
            self.da: self._check_connectivity(self.da)
        }
        if all(results.values()):
            return app
        return False
    def resultados(self):
        return AsserteTrue(db)