Micromodels Riak
------------------
This is a really simple `micromodels <https://github.com/j4mie/micromodels>`_ loader for Riak

Example
========

Here's an example use::

    from micromodelsext.riak import Loader
    import riak
    import micromodels


    class MyModel(micromodels.Model):
        title = micromodels.CharField()


    client = riak.RiakClient()
    bucket = client.bucket("mymodel")

    # create a loader for the bucket and the model
    loader = Loader(bucket, MyModel)
    
    m = MyModel.from_dict({"title": "This is a test"})

    # Store model
    loader['test'] = m

    # Fetch model
    m = loader['test']

    # Delete model
    del loader['test']

Sometimes you want to put scoping information in the bucket's name, but the model will be the same.  For instance::

    
   glenn_entries = Loader(client.bucket("glenn_entries"), MyModel)
   eric_entries = Loader(client.bucket("eric_entries"), MyModel)


   glenn_story = MyModel.from_dict({"title": "I love riding my motorcycle"})
   eric_story = MyModel.from_dict({"title": "I love riding my bicycle"})

   glenn_entries['i-love-my-bike'] = glenn_story
   eric_entries['i-love-my-bike'] = eric_story


The same model is used, but different buckets.

Handling Lists
=================

Riak is a k/v store and this maps nicely to Python dictionaries, however sometimes you have a list of RiakObjects.
Here's an example from a search result using the Riak Search Solr interface::

    bucket = client.bucket("eric_entries")
    loader = Loader(bucket, MyModel)

    result = solr.search("title:bicycle", rows=20)
    obj_gen = (bucket.get(r['id']) for r in result)
    model_list = [loader.cast(obj) for obj in obj_gen]

This actually could be shorten by doing the following::

    bucket = client.bucket("eric_entries")
    loader = Loader(bucket, MyModel)

    result = solr.search("title:bicycle", rows=20)
    model_list = [loader[r['id']] for r in result]



  
