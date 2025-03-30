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
        ("Scraping Post", "How to scrape data from websites using Python and BeautifulSoup.", True)

    ])
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