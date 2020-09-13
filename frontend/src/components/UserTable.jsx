import React, {useRef, useState} from "react"
import {Button, Table, Form} from "react-bootstrap"
import {api} from "../api/api"
import {Redirect} from "react-router"


const AccessSwitch = (props) => {
  const {id, value} = props
  const checkElement = useRef(value)

  const setAccess = async (e) => {
    await api.set_access(e.currentTarget.id).then(data => {
      checkElement.current.checked=data.access
    })
  }


  return (
    <Form.Check
      ref={checkElement}
      onChange={(e) => setAccess(e)}
      checked={value}
      type="switch"
      id={id}
      value={value}
      label=""
    />
  )
}


const UserTable = (props) => {
  const [refresh, setRefresh] = useState(false)
  const {users, isAdmin, currentUserEmail} = props
  const thead = ['#','Email','Token','Hit','Confirmed','Access', 'delete?']

  const confirmDelete = (userId) => {
    const r = window.confirm("Are you sure?")
    if (r === true) {
      api.delete(userId)
        .then(data => {
          if (data?.logout)
            localStorage.removeItem('token')
          setRefresh(true)
        })
    }
  }
  return (
    <>
      {refresh ? <Redirect to='/' /> : ''}
      <Table size="sm" striped bordered hover>
        <thead>
        <tr>
          {thead.map( (i, k) => <th key={k} scope="col">{i}</th> )}
        </tr>
        </thead>
        <tbody>
        {users && users.length > 0 && users.map((item, k) => {
          return (
            <tr key={k}>
              <td>{ item.id}</td>
              <td>{ item.email }</td>
              <td>{ item.token }</td>
              <td>{ item.hit }</td>
              <td>{ item.email_confirmed ? "Yes" : " No" }</td>
              <td>{ isAdmin
                      ? <AccessSwitch id={item.id} value={item.access} />
                      : item.access
                        ? "Yes" : " No" }</td>
              <td>
                {isAdmin
                  ? <Button variant={"danger"} size="sm" onClick={(e) => confirmDelete(item.id)}>del?</Button>
                  : item.email === currentUserEmail && <Button variant={"danger"} size="sm" onClick={(e) => confirmDelete(item.id)}>del?</Button> }
              </td>
            </tr>
          )
        })
        }
        </tbody>
      </Table>
    </>
  )
}


export default UserTable