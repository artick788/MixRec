import React, {useState} from "react";
import {
  Box,
  TextField,
  Typography,
  Grid,
  Button,
  Card,
  CardContent,
  Dialog,
  CardHeader, Collapse, Divider,
  IconButton, DialogTitle, DialogContent, DialogContentText, DialogActions,
  CloseIcon
} from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CircularProgress from "@mui/material/CircularProgress";
import axios from "axios";

export default function ChangeSongPropsDialog(props) {
  const [isOpen, setIsOpen] = useState(false);
  const [song, setSong] = useState(props.song);

  const updateSong = () => {
    axios.patch('http://localhost:8000/apiv1/song/' + song.song_id + '/', song)
      .then((response) => {
        console.log(response);
        setSong(response.data['Song'])
        props.setSong(response.data['Song']);
        setIsOpen(false);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  return (
    <div>
      <Button
        variant="contained"
        sx={{}}
        onClick={() => {setIsOpen(true)}}
      >
        Change Properties
      </Button>
      <Dialog open={isOpen} onClose={() => {setIsOpen(false)}} aria-labelledby="customized-dialog-title">
        <DialogTitle id="customized-dialog-title" onClose={() => {setIsOpen(false)}}>
          Change properties for {song.title} by {song.artist}
        </DialogTitle>
        <DialogContent dividers>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <div>
                <TextField
                  style={{marginBottom: 7}}
                  id="outlined-basic"
                  label="Title"
                  variant="outlined"
                  value={song.title}
                  onChange={(event) => {setSong({...song, title: event.target.value})}}
                />
                <TextField
                  style={{marginBottom: 7}}
                  id="outlined-basic"
                  label="Artist"
                  variant="outlined"
                  value={song.artist}
                  onChange={(event) => {setSong({...song, artist: event.target.value})}}
                />
                <TextField
                  style={{marginBottom: 7}}
                  id="outlined-basic"
                  label="Genre"
                  variant="outlined"
                  value={song.genre}
                  onChange={(event) => {setSong({...song, genre: event.target.value})}}
                />
              </div>
            </Grid>
            <Grid item xs={6}>
              <div style={{margin: 5}}>
                <TextField
                  style={{marginBottom: 7}}
                  id="outlined-basic"
                  label="Album"
                  variant="outlined"
                  value={song.album}
                  onChange={(event) => {setSong({...song, album: event.target.value})}}
                />
                <TextField
                  style={{marginBottom: 7}}
                  id="outlined-basic"
                  label="BPM"
                  variant="outlined"
                  type="number"
                  value={song.bpm}
                  onChange={(event) => {setSong({...song, bpm: event.target.value})}}
                />
                <TextField
                  style={{marginBottom: 7}}
                  id="outlined-basic"
                  label="Key"
                  variant="outlined"
                  value={song.key}
                  onChange={(event) => {setSong({...song, key: event.target.value})}}
                />
              </div>
            </Grid>
          </Grid>
          <TextField
            style={{width: '92%'}}
            id="outlined-basic"
            label="Description"
            variant="outlined"
            value={song.description}
            onChange={(event) => {setSong({...song, description: event.target.value})}}
          />
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={updateSong}>Save changes</Button>
          <Button autoFocus onClick={() => {setIsOpen(false)}}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </div>
  )
}