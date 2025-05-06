from src.tileserver.mbtileserver import create_app


my_app = create_app(
    mbtiles="src/master/chiriin_japan_z2_z9.mbtiles", cache_config={"CACHE_TYPE": "simple"}
)

if __name__ == "__main__":
    #my_app.run(debug=True, port=18888)
    my_app.run(host="100.66.1.13",debug=True, port=18888)
