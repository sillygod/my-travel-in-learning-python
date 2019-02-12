# Ufile Transfer

Transfer all static files links which put in ufile service in our BackendApi Project to another place and change their links. I find there are main source we need to deal with.

 - one is files in our BackendApi project

there are lots of hard coding link in the files.. so we need to extract them first and further, we may need to search and replace the content in those files.

 - the other is DB

# Development

### Env

python3.6

```shell
brew install mysql
brew install libmagic
pip install -r requirement.txt
```


# How to test

# Tasks

 - [x] cli interface
 - [ ] how to test? 
 - [ ] logging?



 `pytest -s test_file` this will make verbose output
 `pytest test_file -k xxx_func` will run specify function


# Note

```python
#we can list blobs in the given bucket
for blob in bucket.list_blobs():
    print(blob.public_url)

test_jpg = bucket.get_blob("avatar/test.jpg")
print(test_jpg.public_url)

file_name = os.path.join(root, "temp.txt")
test txt file

with open(file_name, 'r', encoding='latin-1') as f:
    blob = bucket.blob("legacy/inla.txt")
    blob.upload_from_file(f) # file will be overwritten if exist
    blob.make_public()

```

# Future

Make this tool to be generic.

# References

   - [pytest with docker example](https://docs.pytest.org/en/latest/fixture.html)
