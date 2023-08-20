import React, {useState} from "react";
import {Typography} from "@mui/material";
import axios from "axios";
import SongCard from "./SongCard";


export default function Overview() {
  const [musicList, setMusicList] = useState([]);
  const [fetched, setFetched] = useState(false);

  if (!fetched) {
    axios.get('http://localhost:8000/apiv1/song/')
      .then((response) => {
        console.log(response);
        setMusicList(response.data['Songs']);
        setFetched(true);
        })
      .catch((error) => {
        console.log(error);
      });

    return (
      <div>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}>
          <Typography variant="h4" component="div" gutterBottom>
            Overview
          </Typography>
        </div>
      </div>
      )
  }
  else{
    return (
      <div>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="h4" component="div" gutterBottom>
          Overview
        </Typography>
        {
          musicList.map((song) => {
            return (
              <SongCard song={song} key={song.song_id}/>
            )
          })
        }
      </div>
    </div>
    )
  }
}