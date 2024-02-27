import os
import shutil

import gradio as gr
from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse
from modules.api.models import *
from modules.api import api


GRADIO_CACHE_DIR = os.getenv('GRADIO_CLEANER_DIR', '/temp/gradio')


def sd_gradio_cleaner_api(_: gr.Blocks, app: FastAPI):
    @app.post("/clean_cache")
    async def clean_cache():
        try:
            shutil.rmtree(GRADIO_CACHE_DIR)
        except Exception as e:
            return JSONResponse(
                content=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return JSONResponse(
            content="Ok",
            status_code=status.HTTP_200_OK,
        )

try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(sd_gradio_cleaner_api)
except:
    pass
