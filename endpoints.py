# Spamming with any request or attempts to attack infrastructure will result in team ban.
# PS once we find you, ban won't be your biggest trouble ;P

from typing import List
from dotenv import load_dotenv


import numpy as np
import requests
import os

load_dotenv()

SERVER_URL = "[paste server url here]"
TEAM_TOKEN = "[paste team token here]"


def sybil(ids: List[int], home_or_defense: str, binary_or_affine: str):
    if home_or_defense not in ["home", "defense"] or binary_or_affine not in [
        "binary",
        "affine",
    ]:
        raise Exception("Invalid endpoint")

    endpoint = f"/sybil/{binary_or_affine}/{home_or_defense}"
    url = SERVER_URL + endpoint
    ids = ",".join(map(str, ids))
    response = requests.get(url, params={"ids": ids}, headers={"token": TEAM_TOKEN})
    if response.status_code == 200:
        representations = response.json()["representations"]
        ids = response.json()["ids"]
        print("Request ok", representations, ids)
    else:
        raise Exception(
            f"Sybil failed. Code: {response.status_code}, content: {response.json()}"
        )


# Be careful. This can be done only 4 times an hour.
# Make sure your file has proper content.
def sybil_submit(path_to_npz_file: str, binary_or_affine: str):
    if binary_or_affine not in ["binary", "affine"]:
        raise Exception("Invalid endpoint")

    endpoint = f"/sybil/{binary_or_affine}/submit"
    url = SERVER_URL + endpoint

    with open(path_to_npz_file, "rb") as f:
        response = requests.post(url, files={"file": f}, headers={"token": TEAM_TOKEN})

    if response.status_code == 200:
        print("OK")
        print(response.json())
    else:
        print(
            f"Request submit failed. Status code: {response.status_code}, content: {response.json()}"
        )


def sybil_reset(binary_or_affine: str):
    if binary_or_affine not in ["binary", "affine"]:
        raise Exception("Invalid endpoint")

    endpoint = f"/sybil/{binary_or_affine}/reset"
    url = SERVER_URL + endpoint
    response = requests.post(url, headers={"token": TEAM_TOKEN})
    if response.status_code == 200:
        print("Request ok")
        print(response.json())
    else:
        raise Exception(
            f"Sybil reset failed. Code: {response.status_code}, content: {response.json()}"
        )


# Be careful. This can be done only once an hour.
# Computing this might take a few minutes. Be patient.
# Make sure your file has proper content.
def defense_submit(path_to_npz_file: str):
    endpoint = "/defense/submit"
    url = SERVER_URL + endpoint
    with open(path_to_npz_file, "rb") as f:
        response = requests.post(url, files={"file": f}, headers={"token": TEAM_TOKEN})
        if response.status_code == 200:
            print("Request ok")
            print(response.json())
        else:
            raise Exception(
                f"Defense submit failed. Code: {response.status_code}, content: {response.json()}"
            )


def model_stealing(path_to_png_file: str):
    endpoint = "/modelstealing"
    url = SERVER_URL + endpoint
    with open(path_to_png_file, "rb") as f:
        response = requests.get(url, files={"file": f}, headers={"token": TEAM_TOKEN})
        if response.status_code == 200:
            representation = response.json()["representation"]
            print("Request ok")
            print(representation)
        else:
            raise Exception(
                f"Model stealing failed. Code: {response.status_code}, content: {response.json()}"
            )


def model_stealing_submit(path_to_onnx_file: str):
    endpoint = "/modelstealing/submit"
    url = SERVER_URL + endpoint
    with open(path_to_onnx_file, "rb") as f:
        response = requests.post(url, files={"file": f}, headers={"token": TEAM_TOKEN})
        if response.status_code == 200:
            print("Request ok")
            print(response.json())
        else:
            raise Exception(
                f"Model stealing submit failed. Code: {response.status_code}, content: {response.json()}"
            )


def model_stealing_reset():
    endpoint = f"/modelstealing/reset"
    url = SERVER_URL + endpoint
    response = requests.post(url, headers={"token": TEAM_TOKEN})
    if response.status_code == 200:
        print("Request ok")
        print(response.json())
    else:
        raise Exception(
            f"Model stealing reset failed. Code: {response.status_code}, content: {response.json()}"
        )

# Call examples:

# sybil(
#     [101031, 8526, 43127, 191394, 298792, 121086, 149475, 102605, 163605, 101855],
#     "home",
#     "affine",
# )
# sybil_submit("example_submissions/sybil.npz", "affine")
# sybil_reset("binary")
# defense_submit("example_submissions/defense.npz")
# model_stealing("test.png")
# model_stealing_submit("example_submissions/model_stealing.onnx")
# model_stealing_reset()
