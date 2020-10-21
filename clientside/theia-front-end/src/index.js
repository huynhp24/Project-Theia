import React, { Component } from 'react';
import ReactDOM from "react-dom";


// This code creates a button to upload a file, the clicked file will be store in local storage on the web browser
// open Chrome, run this code by using : npm start
// "Inspect"
// go to "console" to see an object of the file and "Application" to see the saved file
class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            selectedFile: ''
        }
    }

fileSelectedHandler = e =>{
       // this.setState({selectedFile : e.target.files[0]  });
        let myData = e.target.files[0]; //myData is an object that is sellected
        console.log(myData);//print the object in console

            //set data with localStorage
      let test =  JSON.stringify(myData['name']);
      localStorage.setItem('myStorage1', JSON.stringify(test));

};


    componentDidMount() {
          let retrievedObject = localStorage.getItem('myStorage1');
          console.log('retrieved Object is: ', JSON.parse(retrievedObject));
         this.setState({selectedFile :retrievedObject  });

    };
  render() {
    return (

      <div className="App">
          <form>
              <label>Simple Upload Buttons </label>
              <div>
                  <input type="file" onChange={this.fileSelectedHandler} />

              </div>

           </form>
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));
