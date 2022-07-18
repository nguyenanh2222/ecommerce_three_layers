from fastapi import FastAPI
from pydantic import BaseSettings, Field
from app.v1.router import admin, customer


def create_app():
    ...
    return


if __name__ == '__main__':
    create_app()