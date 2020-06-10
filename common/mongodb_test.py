import mongodb_client as client

def test_basic():
    # do not use defualt database which is "tap-news"
    db = client.get_db('test')
    db.test.drop()
    assert db.test.count() == 0
    # insert document which is dictionary
    db.test.insert_one({'test': 1})
    assert db.test.count() == 1
    # clean up
    db.test.drop()
    assert db.test.count() == 0
    print('test_basic passed.')

# only run through command line
if __name__ == "__main__":
    test_basic()
