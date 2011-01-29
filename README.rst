Micromodels Riak
------------------
This is a really simple micromodels loader for Riak

Example
========

Here's an example use::

    from micromodelsext.riak import Loader
    import riak
    import micromodels


    class MyModel(micromodels.Model):
        title = micromodels.CharField()


    loader = Loader(riak.RiakClient().bucket("mymodel"), MyModel)
    
    m = MyModel.from_dict({"title": "This is a test"})

    # Store model
    loader['test'] = m

    # Fetch model
    m = loader['test']

    # Delete model
    del loader['test']
