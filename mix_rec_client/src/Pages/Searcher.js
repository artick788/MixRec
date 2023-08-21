import React from "react";
import {Box, Button, Grid, TextField, Typography} from "@mui/material";
import axios from "axios";


export default function Searcher() {
  const [query, setQuery] = React.useState("" );

  const submit = () => {
    axios.get('http://localhost:8000/apiv1/search/' + query + "/",)
      .then((response) => {
        console.log(response);
        })
      .catch((error) => {
        console.log(error);
      });
  }

  return (
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
  );
}