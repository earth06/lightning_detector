import argparse

from src.tileserver.mbtileserver import create_app

my_app = create_app(mbtiles="src/master/chiriin_japan_z2_z9.mbtiles", cache_config={"CACHE_TYPE": "simple"})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost", help="server's IP 100.66.1.13")
    parser.add_argument("--port", default=18888, help="port number")
    # my_app.run(debug=True, port=18888)
    my_app.run(host="100.66.1.13", debug=True, port=18888)
