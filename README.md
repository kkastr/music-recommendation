# Spotify Music Recommender

## Setup

Install the required libraries for this project by running the following in the terminal:

```bash
pip install requirements.txt
```

This will only install `kaggle` and `spotipy` as it is assumed standard python libraries such as `numpy`, `pandas`, `sklearn` etc. are already installed.

The data used in this project is from [this kaggle dataset](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db).

To download the data from the terminal, first follow the instructions found [here](https://www.kaggle.com/docs/api) and set up the kaggle CLI. After the previous instructions are complete, run the following in the terminal:

```bash
kaggle datasets download -d zaheenhamidani/ultimate-spotify-tracks-db
```

This project uses [spotipy](https://spotipy.readthedocs.io/en/master/) to interface with the Spotify web API, and as such requires an spotify developer app client id and client id.

To obtain your client id and client secret navigate to the [spotify developer dashboard](https://spotipy.readthedocs.io/en/master/) and create an app. After the app is created you should be able to recover the relevant keys.

After the keys are obtained, place the lines below in a file called `api_keys.py`.

```python
client_id = "your-client-id"
client_secret = "your-client-secret"
```

## Usage

Place tracks (along with their artist) that you wish to find similar music to in the `input_tracklist.py` file.

After having done that, run the following in the terminal to get a list of five recommended tracks:

```bash
python recommender.py
```

## Limitations

The dataset has a limited set of genres and tracks. As a result, if you look for songs similar to e.g. some types of metal, you will get very strange recommendations. Might refactor if I find a more comprehensive dataset.
