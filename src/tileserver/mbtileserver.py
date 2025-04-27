from flask import Flask, g, abort, Blueprint, current_app, Response
from flask_cors import CORS
from flask_caching import Cache
import os
import sqlite3

frontend = Blueprint('frontend', __name__)
cache = Cache()


@frontend.before_request
def before_request() -> None:
    """Ensure database is connected for each request."""
    g.db = sqlite3.connect(current_app.config['MBTILES_PATH'])


@frontend.teardown_request
def teardown_request(exception: Exception = None) -> None:
    """Cleanup database afterwards."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


@frontend.route("/<int:z>/<int:x>/<int:y>.png")
@cache.cached(timeout=300)
def query_tile(z: int, x: int, y: int) -> Response:
    """Get a tile from the MBTiles database."""
    flip_y = (2**z -1) - y
    flip_x = (2**z-1) - x
    query = '''
        SELECT tile_data FROM tiles
        WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?;
    '''
    cursor = g.db.execute(query, (z,x, flip_y))
    result = cursor.fetchone()
    print(z,flip_x, flip_y)    
    if result is None:
        abort(404)
    tile_data = result[0]

    return Response(tile_data, mimetype='image/png')


def create_app(mbtiles: str, cache_config: dict = None) -> Flask:
    """Initialize the application with a given configuration."""
    app = Flask(__name__)
    app.config['MBTILES_PATH'] = mbtiles
    cache.init_app(app, config=cache_config or {'CACHE_TYPE': 'simple'})
    app.register_blueprint(frontend)
    # ヘッダがないとplotly側で画像を受け取らなくなるらしい
    CORS(app)
    return app


if __name__ == "__main__":
    mbtiles_path = os.environ.get('MBTILES_PATH')
    port = int(os.environ.get('MBTILES_PORT', 41815))
    if not mbtiles_path:
        raise EnvironmentError("Environment variable MBTILES_PATH must be set.")

    app = create_app(mbtiles=mbtiles_path)
    app.run(debug=True, port=port)