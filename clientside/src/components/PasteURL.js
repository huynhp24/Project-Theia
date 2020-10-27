import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
}));

export default function PasteURL() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
        <form className={classes.root} noValidate autoComplete="off">
            <TextField id="outlined-basic" label="Paste image URL" variant="outlined" />
        </form>
        <Button variant="contained" color="primary" href="#contained-buttons">
                Search by image
        </Button>
    </div>
  );
}