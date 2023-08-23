import React, {useState} from "react";
import {
  Box,
  TextField,
  Typography,
  Grid,
  Button,
  Card,
  CardContent,
  CardHeader, Collapse, Divider,
} from "@mui/material";
import {IconButton} from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CircularProgress from "@mui/material/CircularProgress";

export default function SongCard(props) {
  const [expanded, setExpanded] = useState(false);
  const [song, setSong] = useState(props.song);

  return (
    <Card sx={{ width: '70%', marginBottom: 1 }}>
      <CardHeader
        title={song.title}
        subheader={song.artist}
        action={
          <IconButton onClick={() => {setExpanded(!expanded)}}>
            <ExpandMoreIcon />
          </IconButton>
        }
      />
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          <Divider />
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <p>Description: {song.description}</p>
            {song.score !== undefined && <p>Score: {song.score.toFixed(2)}</p>}
          </div>
          <Divider />
          <div style={{textAlign: 'left'}}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <div>
                  <p>Genre: {song.genre}</p>
                  <p>Album: {song.album}</p>
                  <p>Duration: {song.duration}</p>
                </div>
              </Grid>
              <Grid item xs={6}>
                <div>
                  <p>BPM: {song.bpm}</p>
                  <p>Key: {song.key}</p>
                  <p>Camelot: {song.camelot_key}</p>
                </div>
              </Grid>
            </Grid>
          </div>
          <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginRight: '20px' }}>
              <CircularProgress
                variant="determinate"
                value={song.acousticness}
              />
              <p>Acousticness: {song.acousticness}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginRight: '20px' }}>
              <CircularProgress
                variant="determinate"
                value={song.danceability}
              />
              <p>Danceability: {song.danceability}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginRight: '20px' }}>
              <CircularProgress
                variant="determinate"
                value={song.energy}
              />
              <p>Energy: {song.energy}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginRight: '20px' }}>
              <CircularProgress
                variant="determinate"
                value={song.happiness}
              />
              <p>Happiness: {song.happiness}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginRight: '20px' }}>
              <CircularProgress
                variant="determinate"
                value={song.instrumentalness}
              />
              <p>Instrumentalness: {song.instrumentalness}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginRight: '20px' }}>
              <CircularProgress
                variant="determinate"
                value={song.liveness}
              />
              <p>Liveness: {song.liveness}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginRight: '20px' }}>
              <CircularProgress
                variant="determinate"
                value={song.popularity}
              />
              <p>Popularity: {song.popularity}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginRight: '20px' }}>
              <CircularProgress
                variant="determinate"
                value={song.speechiness}
              />
              <p>Speechiness: {song.speechiness}</p>
            </div>
          </div>
        </CardContent>
      </Collapse>
    </Card>
  )
}