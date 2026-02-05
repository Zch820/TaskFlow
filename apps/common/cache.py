import json
import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def cache_project_page(projects, user_id, page, start, end):
    """
    Cash projects values and return them in a list form.
    ( values : id, name, created_at )
    """
    projects = projects.values("id", "name", "created_at")[start:end]
    project_list = [{"id": p["id"], "name": p["name"], "created_at": p["created_at"].isoformat()} for p in projects]
    r.setex(f"user:{user_id}:projects:{page}", 60*30, json.dumps(project_list))
    return project_list


def get_or_cache_project_page(projects, user_id, page, start, end):
    """
    Return cached project data from redis db,
    otherwise call and return cache_project_page().
    ( values : id, name, created_at )
    """
    try:
        cached = r.get(f"user:{user_id}:projects:{page}")
        if cached:
            return json.loads(cached)
    except redis.RedisError:
        pass

    return cache_project_page(projects, user_id, page, start, end)
