import React from 'react';
import ReactDOM from 'react-dom';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';

import ReactS3, { uploadFile } from 'react-s3';

const useStyles = makeStyles((theme) => ({
    root: {
      '& > *': {
        margin: theme.spacing(1),
      },
    },
    input: {
      display: 'none',
    },
  }));


const config = {
  bucketName: 'project-theia-test',
  // dirName: 'nhiphotos', /* optional album name */
  region: 'us-west-1',
  accessKeyId: '',
  secretAccessKey: '',
};

  export default function UploadButtons() {

    const classes = useStyles();

    function uploadFile(e) {
      console.log(e.target.files[0]);
      ReactS3.uploadFile( e.target.files[0] , config)
      .then( (data)=>{
        console.log(data.location);
      })
      .catch( (err)=>{
        alert(err);
      })
    }

    return (
      <div className={classes.root}>
        <input
          accept="image/png, image/jpeg" //limit only certain image types: PNG, JPEG
          className={classes.input}
          id="contained-button-file"
          multiple={false} //allows only one image to be uploaded at a time
          type="file"
          maxFileSize={5242880} //max image size is 5MB

          onChange={uploadFile}
        />
        <label htmlFor="contained-button-file">
            <Button variant="contained" color="primary" component="span" startIcon={<CloudUploadIcon />}>
                Choose File
            </Button>
        </label>
      </div>
    );
  }
