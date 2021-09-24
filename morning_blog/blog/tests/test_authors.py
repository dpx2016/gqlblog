import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from graphene.test import Client

from blog.models import Author, Blog
from blog.schema.blogs import schema

author_list_query = """
    query {
        authors {
            id
            name
            description 
        }
    }
"""

single_author_query = """
    query($id:ID!)
    {
        author(id:$id) {
            id
            name
            description
        }
    }
"""

create_author_mutation = """
     mutation CreateAuthor($input: AuthorInputType!) {
        createAuthor(input: $input) {
            author {
                id
                name
                description
            }
            ok
        }
    }
"""

update_author_mutation = """
     mutation UpdateAuthor($input: AuthorInputType!) {
        updateAuthor(input: $input) {
            author {
                id
                name
            }
            ok
        }
    }
"""

delete_author_mutation = """
    mutation DeleteAuthor($input: DeleteAuthorInputType!) {
        deleteAuthor(input: $input) {
            ok
        }
    }
"""


@pytest.mark.django_db
class TestAuthorSchema(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.author = mixer.blend(Author)

    def test_single_author_query(self):
        response = self.client.execute(single_author_query, variables={"id": self.author.id})
        response_author = response.get("data").get("author")
        assert response_author["id"] == str(self.author.id)

    def test_author_list_query(self):
        mixer.blend(Author)
        mixer.blend(Author)

        response = self.client.execute(author_list_query)
        authors = response.get("data").get("authors")
        ok = response.get("data").get("ok")

        assert len(authors)