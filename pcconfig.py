import pynecone as pc

config = pc.Config(
    app_name="smart_farm",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
