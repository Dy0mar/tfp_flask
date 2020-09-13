import React from "react"
import {Nav, Navbar} from "react-bootstrap"

import {NavLink} from "react-router-dom"

const Header = () => {
  return (
      <Navbar bg="dark" variant="dark">
        <Nav className="mr-auto" defaultActiveKey={'/home'}>
          <Nav.Link as={NavLink} to="/home">Home</Nav.Link>
          <Nav.Link as={NavLink} to="/get-access">Get Access</Nav.Link>
        </Nav>
      </Navbar>
  )
}

export default Header