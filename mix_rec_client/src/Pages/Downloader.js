import React, {useState} from "react";
import {Box, TextField, Typography, Grid, Button} from "@mui/material";
import axios from "axios";


export default function Downloader() {
  const [url, setUrl] = useState("");
  const [artist, setArtist] = useState("");
  const [title, setTitle] = useState("");
  const [album, setAlbum] = useState("");
  const [genre, setGenre] = useState("");

  const download = () => {
    const body = {
      url: url,
      artist: artist,
      title: title,
      album: album,
      genre: genre,
      option: 'download'
    };

    axios.post('http://localhost:8000/apiv1/song/', body)
      .then((response) => {
        console.log(response);
        }).
      catch((error) => {
        console.log(error);
      });
  }

  return (
    <div>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh', // Ensures the div covers the full viewport height
      }}>
        <Box sx={{ width: '100%' }}>
          <Grid container spacing={2}>

            <Grid item xs={12}>
              <Typography variant="h4" component="div" gutterBottom>
                Download
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <TextField
                id="url"
                label="URL"
                variant="outlined"
                value={url}
                sx={{ width: '30%' }}
                onChange={(event) => setUrl(event.target.value)}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                id="artist"
                label="Artist"
                variant="outlined"
                value={artist}
                sx={{ width: '30%' }}
                onChange={(event) => setArtist(event.target.value)}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                id="title"
                label="Title"
                variant="outlined"
                value={title}
                sx={{ width: '30%' }}
                onChange={(event) => setTitle(event.target.value)}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                id="album"
                label="Album"
                variant="outlined"
                value={album}
                sx={{ width: '30%' }}
                onChange={(event) => setAlbum(event.target.value)}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                id="genre"
                label="Genre"
                variant="outlined"
                value={genre}
                sx={{ width: '30%' }}
                onChange={(event) => setGenre(event.target.value)}
              />
            </Grid>

            <Grid item xs={12}>
              <Button
                variant="contained"
                sx={{ width: '30%' }}
                onClick={download}
              >
                Download
              </Button>
            </Grid>
          </Grid>
        </Box>
      </div>
    </div>
  );
}