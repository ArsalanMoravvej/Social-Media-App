
def test_vote_on_post(authorized_client, test_posts):
    payload = {
        "post_id": test_posts[3].id,
        "dir": 1
        }
    response = authorized_client.post(f'/vote/', json=payload)
    assert response.status_code == 201

def test_vote_on_post_twice(authorized_client, test_posts):
    payload = {
        "post_id": test_posts[3].id,
        "dir": 1
        }
    response = authorized_client.post(f'/vote/', json=payload)
    assert response.status_code == 201
    response = authorized_client.post(f'/vote/', json=payload)
    assert response.status_code == 409
    