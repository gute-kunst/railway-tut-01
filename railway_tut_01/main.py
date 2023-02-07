from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_main():
    return """
    <html>
        <body>
            <h1>Fancy Surface Reconstruction App</h1>
        </body>
    </html>
    """
