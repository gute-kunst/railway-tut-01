import aiofiles
from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

import algorithm as alg

app = FastAPI()
import os

import uvicorn
from starlette.responses import FileResponse

INPUT_FILE_PATH = "./tmp/pc.vtp"
OUTPUT_FILE_PATH = "./tmp/surface.stl"


@app.get("/", response_class=HTMLResponse)
async def main():
    return """
        <head>
        <script async defer data-website-id="a0afcde6-cfaa-4a2a-b1a4-84dede35163a" src="https://umami-production-8332.up.railway.app/umami.js"></script>
        </head>
        <body>
            <h1>Fancy Surface Reconstruction App</h1>                

            <form action="/process/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="number" placeholder="cell size" name="cellsize" step="any" min=0 max=1/>
                <input type="submit">
            </form>
        </body>
    """


def surface_pipeline(input_file_path, output_file_path, cell_size, alpha=0.5):
    polydata = alg.load_vtp(input_file_path)
    nbr_cells, grid_minimum = alg.get_configuration(polydata, cell_size, cell_size)
    grid = alg.vtk_image_data(grid_minimum, cell_size, nbr_cells)
    retval_interpolate = alg.sph(cell_size, grid, polydata)
    retval = alg.contour(retval_interpolate, alpha)
    alg.save_stl(output_file_path, retval)


@app.post("/process/")
async def create_upload_file(file: UploadFile, cellsize: float = Form()):
    if not os.path.isdir("tmp"):
        os.makedirs("tmp")
    async with aiofiles.open(INPUT_FILE_PATH, "wb") as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    surface_pipeline(INPUT_FILE_PATH, OUTPUT_FILE_PATH, cellsize)
    return FileResponse(OUTPUT_FILE_PATH, filename="surface.stl", media_type="binary")


import os

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT")))
