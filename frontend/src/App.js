import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'
import './App.css'
import {BrowserRouter} from "react-router-dom"
import {Switch, Route, Redirect} from "react-router"

import {Container, Row} from "react-bootstrap"

import Header from "./components/Header"
import Home from "./components/Home"
import GetAccess from "./components/GetAccess"
import CheckConfirm from "./components/ConfirmPage"


class NotFound extends React.Component{
  render(){
    return <h2>Ресурс не найден</h2>
  }
}



function App() {
  return (
    <BrowserRouter>
      <Header />
      <Container>
        <Row className="justify-content-md-center" style={{margin: 30 }}>
          <Switch>

            <Route path='/home' render={() => <Home />} />
            <Route path='/get-access' render={() => <GetAccess />} />
            <Route path='/confirm/:token?' render={() => <CheckConfirm />} />

            <Redirect exact from="/" to="/home" />
            <Route component={NotFound} />
          </Switch>
        </Row>
      </Container>
    </BrowserRouter>
  )
}

export default App
