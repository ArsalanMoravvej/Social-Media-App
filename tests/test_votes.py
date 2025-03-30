import pytest

@pytest.fixture
def test_vote(authorized_client, test_posts):
    post_id = test_posts[3].id  # Extract ID before potential session closure
    payload = {
        "post_id": post_id,
        "dir": 1
    }
    authorized_client.post('/vote/', json=payload)
    return post_id

def test_vote_unauthorized(client, test_posts):
    payload = {
        "post_id": test_posts[3].id,
        "dir": 1
    }
    response = client.post('/vote/', json=payload)
    assert response.status_code == 401

def test_vote_on_post(authorized_client, test_posts):
    payload = {
        "post_id": test_posts[3].id,
        "dir": 1
        }
    response = authorized_client.post(f'/vote/', json=payload)
    assert response.status_code == 201

def test_vote_on_post_twice(authorized_client, test_posts, test_vote):

    response = authorized_client.post(
        '/vote/', json={"post_id": test_vote, "dir": 1}
        )
    assert response.status_code == 409

def test_delete_vote(authorized_client, test_vote):
    payload = {
        "post_id": test_vote,
        "dir": 0
        }
    response = authorized_client.post('/vote/', json=payload)
    assert response.status_code == 201

def test_delete_vote_twice(authorized_client, test_posts):
    payload = {
        "post_id": test_posts[3].id,
        "dir": 0
        }
    response = authorized_client.post('/vote/', json=payload)
    assert response.status_code == 404

def test_vote_on_non_existing_post(authorized_client):
    payload = {
        "post_id": 9999,
        "dir": 1
        }
    response = authorized_client.post('/vote/', json=payload)
    assert response.status_code == 404