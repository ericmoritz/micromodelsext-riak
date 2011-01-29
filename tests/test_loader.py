import riak
from micromodelsext.riak import Loader
import micromodels
import unittest


class MyModel(micromodels.Model):
    title = micromodels.CharField()

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.test_key = "testkey"
        self.bucket = riak.RiakClient().bucket("__test__")

        # Amp up the consistancy so that the tests will pass
        self.bucket.set_r(1)
        self.bucket.set_w(3) 
        
        # Clean the slate
        obj = self.bucket.new(self.test_key)
        obj.delete()

    def test_set(self):
        loader = Loader(self.bucket, MyModel)

        data = {'title': "This is a test, this is only a test"}

        
        # Store the model
        m = MyModel.from_dict(data)
        loader[self.test_key] = m
        
        # Assert that the data was stored
        obj = self.bucket.get(self.test_key)
        self.assertEqual(obj.get_data(), data)

    def test_delete(self):
        loader = Loader(self.bucket, MyModel)

        # Put some data into the bucket
        obj = self.bucket.new(self.test_key, data="Something")
        obj.store()

        # Assert the data exists
        self.assertTrue(self.bucket.get(self.test_key).exists())
        
        # Delete the key using the loader
        del loader[self.test_key]

        # Assert that the data no longer exists
        self.assertFalse(self.bucket.get(self.test_key).exists())
    
    def test_get(self):
        loader = Loader(self.bucket, MyModel)

        # Store some data into the datastore
        data = {"title": "This is a test"}
        obj = self.bucket.new(self.test_key, data=data)
        obj.store()

        # Load the model using the loader
        m = loader[self.test_key]

        # Assert that the model data is the same as the data stored
        self.assertEqual(m.to_dict(serial=True), data)
        
    def test_get_wrong_type(self):
        """Test what happens when the stored data mismatches the model's schema"""
        # Store some data into the datastore
        loader = Loader(self.bucket, MyModel)

        data = "Oh Knowes, I'm not a dict"
        obj = self.bucket.new(self.test_key, data=data)
        obj.store()
        
        # Not sure what will happen
        m = loader[self.test_key]
        
    def test_get_wrong_data(self):
        """Test what happens when the stored data mismatches the model's schema"""
        # Store some data into the datastore
        loader = Loader(self.bucket, MyModel)

        data = {"not-title": "This is not the title"}
        obj = self.bucket.new(self.test_key, data=data)
        obj.store()
        
        # Not sure what will happen
        m = loader[self.test_key]

        self.assertEqual(m.to_dict(serial=True), {})

if __name__ == '__main__':
    unittest.main()
