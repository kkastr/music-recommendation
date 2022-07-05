import numpy as np
import pandas as pd
import spotipy as sp
from input_tracklist import input_tracks, input_artists
from scipy.spatial.distance import cdist
from api_keys import client_id, client_secret
from sklearn.preprocessing import StandardScaler
from spotipy.oauth2 import SpotifyClientCredentials


def search_for_track(track: str, artist: str) -> pd.DataFrame:

    # search for track in case it does not exist in dataset

    api_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    spotify = sp.Spotify(auth_manager=api_credentials)

    query = f"track: {track} artist: {artist}"
    response = spotify.search(q=query, limit=1)  # returns dict

    response = response["tracks"]["items"]  # get list of tracks

    if not response:
        return None
    else:
        response = response[0]  # get first track in list

    audio_features = spotify.audio_features(response["id"])

    ret_df = pd.DataFrame.from_dict(audio_features)

    ret_df["track_name"] = response["name"]
    ret_df["popularity"] = response["popularity"]
    ret_df["artist_name"] = response["artists"][0]["name"]

    return ret_df


def get_track_data(track: str, artist: str, sdf: pd.DataFrame) -> pd.DataFrame:

    if track in sdf.track_name.to_list():
        query = f'track_name == "{track}" and artist_name == "{artist}"'

        track_data = sdf.query(query).select_dtypes(np.number).head(1)

        track_data["idx"] = track_data.index.values
        return track_data
    else:
        result = search_for_track(track=track, artist=artist)

        track_data = result.select_dtypes(np.number)

        track_data["idx"] = np.nan
        return track_data


def get_vectors(tdf: pd.DataFrame, sdf: pd.DataFrame):
    tmp = []

    for row in tdf.itertuples():
        vector = get_track_data(row.track, row.artist, sdf)
        tmp.append(vector)

    vdf = pd.concat(tmp, ignore_index=True)
    vdf.drop(columns=["key", "time_signature", "mode"], inplace=True)
    return vdf


def get_recommendations(tdf: pd.DataFrame, sdf: pd.DataFrame, nrecs: int = 5) -> pd.DataFrame:
    track_vectors = get_vectors(tdf, sdf)

    num_sdf = sdf.select_dtypes(np.number)

    scaler = StandardScaler()
    scaler.fit(num_sdf)

    for i in track_vectors.idx:
        if not np.isnan(i):
            sdf.drop(index=i, inplace=True)

    track_vectors.drop(columns="idx", inplace=True)

    scaled_data = scaler.transform(num_sdf)

    mean_vector = track_vectors.mean().to_frame().T

    scaled_mean_vector = scaler.transform(mean_vector)

    cos_dists = cdist(scaled_mean_vector, scaled_data, "cosine").flatten()

    rec_index = np.argsort(cos_dists)[:nrecs]

    return sdf.iloc[rec_index]


def main():

    df = pd.read_csv("spotify_dataset.csv")

    input_params = dict(track=input_tracks, artist=input_artists)

    tdf = pd.DataFrame(data=input_params)

    recommendation = get_recommendations(tdf=tdf, sdf=df)

    print(recommendation[["track_name", "artist_name", "genre"]])


if __name__ == "__main__":
    main()
