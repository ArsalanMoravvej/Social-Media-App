import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts")

    def valid_post(post):
        return schemas.PostOut(**post)
    
    posts_map = map(valid_post, response.json())
    posts_list = list(posts_map)

    assert len(posts_list) == len(test_posts)
    assert response.status_code == 200

def test_unauthorized_get_all_posts(client, test_posts):
    response = client.get("/posts")
    assert response.status_code == 401
