import React from "react";
import {Box, Button, Grid, TextField, Typography} from "@mui/material";
import axios from "axios";
import SongCard from "./SongCard";


export default function Searcher() {
  const [query, setQuery] = React.useState("" );
  const [k, setK] = React.useState(10);
  const [musicList, setMusicList] = React.useState([]);
  const [scores, setScores] = React.useState([]);

  const submit = () => {
    if (query === "" || k < 1) {
      return;
    }
    const body = {
      query: query,
      k: k
    }
    axios.post('http://localhost:8000/apiv1/search/', body)
      .then((response) => {
        const songs = response.data['Songs'];
        for (let i = 0; i < songs.length; i++) {
          songs[i]['score'] = response.data['Scores'][i];
        }
        console.log(songs);
        // sort songs by score from high to low
        songs.sort((a, b) => {
          return b.score - a.score;
        })
        setMusicList(songs);
        })
      .catch((error) => {
        console.log(error);
      });
  }

  return (
    <div>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}>
        <Box sx={{ width: '100%' }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="h4" component="div" gutterBottom>
                Searcher
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <TextField
                id="Query"
                label="Query"
                variant="outlined"
                value={query}
                sx={{ width: '30%' }}
                onChange={(event) => setQuery(event.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                id="K"
                label="K"
                variant="outlined"
                type="number"
                value={k}
                sx={{ width: '30%' }}
                onChange={(event) => setK(event.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                variant="contained"
                sx={{ width: '30%' }}
                onClick={submit}
              >
                Submit
              </Button>
            </Grid>
          </Grid>
       </Box>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {
          musicList.map((song) => {
            return (
              <SongCard song={song} key={song.song_id}/>
            )
          })
        }
      </div>
    </div>
  );
}