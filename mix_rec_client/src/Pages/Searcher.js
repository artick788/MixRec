import React from "react";
import {Box,
  Button,
  Grid,
  TextField,
  Typography,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
} from "@mui/material";
import axios from "axios";
import SongCard from "./SongCard";


export default function Searcher() {
  const [query, setQuery] = React.useState("" );
  const [k, setK] = React.useState(10);
  const [method, setMethod] = React.useState("TF-IDF");
  const [similarity, setSimilarity] = React.useState("Cosine");

  const [musicList, setMusicList] = React.useState([]);

  const submit = () => {
    if (query === "" || k < 1) {
      return;
    }
    const body = {
      query: query,
      k: k,
      method: method,
      similarity_method: similarity,
    }
    axios.post('http://localhost:8000/apiv1/search/', body)
      .then((response) => {
       const songs = response.data['Songs'].map((song, index) => ({
          ...song,
          score: response.data['Scores'][index]
        }));
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
            <Grid item xs={12} >
              <FormControl sx={{ width: '30%' }}>
                <InputLabel id="method-picker">Method</InputLabel>
                <Select
                  labelId="method-picker"
                  id="method-picker"
                  value={method}
                  label="Method"
                  onChange={(e) => setMethod(e.target.value)}
                >
                  <MenuItem value="TF-IDF">TF-IDF</MenuItem>
                  <MenuItem value="LSI">LSI</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            {
              method === "TF-IDF" && (
                <Grid item xs={12}>
                  <FormControl sx={{ width: '30%' }}>
                    <InputLabel id="similarity-method-picker">Similarity Method</InputLabel>
                    <Select
                      labelId="similarity-method-picker"
                      id="similarity-method-picker"
                      value={similarity}
                      label="Similarity Method"
                      onChange={(e) => setSimilarity(e.target.value)}
                    >
                      <MenuItem value="Cosine">Cosine</MenuItem>
                      <MenuItem value="Euclidean">Euclidean</MenuItem>
                      <MenuItem value="Manhattan">Manhattan</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              )
            }
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