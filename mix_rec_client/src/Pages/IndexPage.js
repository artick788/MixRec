import React, {useState} from "react";
import {
  Box,
  Button,
  Grid,
  TextField,
  Typography,
  MenuItem,
  FormControl,
  InputLabel,
  Select, Divider, List, ListItem
} from "@mui/material";
import axios from "axios";
import SongCard from "./SongCard";
import CircularProgress from "@mui/material/CircularProgress";

export default function IndexPage(){
  const [norm, setNorm] = React.useState("l2");
  const [useIDF, setUseIDF] = React.useState("True");
  const [smoothIDF, setSmoothIDF] = React.useState("True");
  const [sublinearTF, setSublinearTF] = React.useState("False");
  const [minDF, setMinDF] = React.useState(1);
  const [maxDF, setMaxDF] = React.useState(1.0);
  const [recreatingIndex, setRecreatingIndex] = useState(false);

  const createIndex = () => {
    const body = {
      norm: norm,
      use_idf: useIDF,
      smooth_idf: smoothIDF,
      sublinear_tf: sublinearTF,
      min_df: minDF,
      max_df: maxDF,
    }
    setRecreatingIndex(true);
     axios.post('http://localhost:8000/apiv1/index/', body)
      .then((response) => {
        setRecreatingIndex(false);
        })
      .catch((error) => {
        console.log(error);
      });
  }

  const spinnerOrRecreatingIndex = () => {
    if (!recreatingIndex){
      return (
        <Button
          variant="contained"
          sx={{ width: '30%' }}
          onClick={createIndex}
        >
          Create Index
        </Button>
      )
    }
    else{
      return (
        <CircularProgress />
      )
    }
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
                Index Configuration
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="h5" component="div" gutterBottom>
                TF-IDF
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <FormControl sx={{ width: '30%' }}>
              <InputLabel id="normalization-method">Normalization Method</InputLabel>
                <Select
                  labelId="normalization-method"
                  id="normalization-method"
                  value={norm}
                  label="Similarity Method"
                  onChange={(e) => setNorm(e.target.value)}
                >
                  <MenuItem value="l2">Squares</MenuItem>
                  <MenuItem value="l1">Absolute</MenuItem>
                  <MenuItem value="None">None</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl sx={{ width: '30%' }}>
                <InputLabel id="use-idf">Use IDF</InputLabel>
                <Select
                  labelId="use-idf"
                  id="use-idf"
                  value={useIDF}
                  label="Use IDF"
                  onChange={(e) => setUseIDF(e.target.value)}
                >
                  <MenuItem value="True">True</MenuItem>
                  <MenuItem value="False">False</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl sx={{ width: '30%' }}>
                <InputLabel id="smooth-idf">Smooth IDF</InputLabel>
                <Select
                  labelId="smooth-idf"
                  id="smooth-idf"
                  value={smoothIDF}
                  label="Smooth IDF"
                  onChange={(e) => setSmoothIDF(e.target.value)}
                >
                  <MenuItem value="True">True</MenuItem>
                  <MenuItem value="False">False</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl sx={{ width: '30%' }}>
                <InputLabel id="sublinear-tf">Sublinear TF</InputLabel>
                <Select
                  labelId="sublinear-tf"
                  id="sublinear-tf"
                  value={sublinearTF}
                  label="Sublinear TF"
                  onChange={(e) => setSublinearTF(e.target.value)}
                >
                  <MenuItem value="True">True</MenuItem>
                  <MenuItem value="False">False</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                id="min-df"
                label="Min DF"
                variant="outlined"
                type="number"
                value={minDF}
                sx={{ width: '30%' }}
                onChange={(event) => setMinDF(event.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                id="max-df"
                label="Max DF"
                variant="outlined"
                type="number"
                value={maxDF}
                sx={{ width: '30%' }}
                onChange={(event) => setMaxDF(event.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              {
                spinnerOrRecreatingIndex()
              }
            </Grid>
          </Grid>
        </Box>
      </div>
    </div>
  )
}