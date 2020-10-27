import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import InsertLinkIcon from '@material-ui/icons/InsertLink';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import UploadButtons from './UploadButtons';
import PasteURL from './PasteURL';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`scrollable-prevent-tabpanel-${index}`}
      aria-labelledby={`scrollable-prevent-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `scrollable-prevent-tab-${index}`,
    'aria-controls': `scrollable-prevent-tabpanel-${index}`,
  };
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    width: '100%',
    backgroundColor: theme.palette.background.paper,
  },
}));

export default function ScrollableTabsButtonPrevent() {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Tabs
          value={value}
          onChange={handleChange}
          variant="scrollable"
          scrollButtons="off"
          indicatorColor="secondary"
          textColor="white"
          aria-label="scrollable prevent tabs example"
        >
          <Tab icon={<CloudUploadIcon />} aria-label="upload" {...a11yProps(0)} label="Upload an image" />
          <Tab icon={<InsertLinkIcon />} aria-label="link" {...a11yProps(1)} label="Paste image URL"/>
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {/* Upload an image */}
        <UploadButtons />
      </TabPanel>
      <TabPanel value={value} index={1}>
        {/* Paste image URL */}
        <PasteURL />
      </TabPanel>
    </div>
  );
}
