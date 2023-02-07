from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
import uvicorn


@app.get("/", response_class=HTMLResponse)
async def read_main():
    return """
    <html>
        <body>
            <h1>Fancy Surface Reconstruction App</h1>
        </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port="$PORT")
