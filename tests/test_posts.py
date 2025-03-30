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

def test_get_single_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    post = schemas.PostOut(**response.json())
    assert post.Post.id == test_posts[0].id

def test_unauthorized_get_single_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post_not_exists(authorized_client, test_posts):
    response = authorized_client.get("/posts/100")
    assert response.status_code == 404

@pytest.mark.parametrize(
    "title, content, published", [
        ("New Post", "This is a new post.", True),
        ("Unpublished Post", "UpdThis is an unpublished post.", False),
        ("Pizza Post", "Delicious pizza recipes and tips!", True),
        ("Scraping Post", "How to scrape data from websites using Python and BeautifulSoup.", True)])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post("/posts", json={"title": title,
                                                      "content": content,
                                                      "published": published})
    
    assert response.status_code == 201
    
    post = schemas.PostResponse(**response.json())
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == test_user['id']

def test_create_post_default_published(authorized_client, test_user):
    response = authorized_client.post("/posts", json={"title": "Default Published Post",
                                                      "content": "This is a default published post."})
    assert response.status_code == 201
    post = schemas.PostResponse(**response.json())
    assert post.published == True

def test_unauthorized_create_post(client):
    response = client.post("/posts", json={"title": "Unauthorized Post",
                                                      "content": "This is an unauthorized post.",
                                                      "published": True})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert "access_token" not in response.json()

def test_unauthorized_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_not_exists(authorized_client, test_posts):
    response = authorized_client.delete("/posts/100")
    assert response.status_code == 404

def test_unauthorized_update_post(client, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}", json={"title": "Unauthorized Post",
                                                              "content": "This is an unauthorized post."})
    assert response.status_code == 401

def test_update_post(authorized_client, test_posts):
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json={"title": "Updated Post",
                                                              "content": "This is an updated post."})
    assert response.status_code == 200
    post = schemas.PostResponse(**response.json())
    assert post.title == "Updated Post"
    assert post.content == "This is an updated post."

def test_update_post_not_exists(authorized_client, test_posts):
    response = authorized_client.put("/posts/100", json={"title": "Updated Post",
                                                              "content": "This is an updated post."})
    assert response.status_code == 404