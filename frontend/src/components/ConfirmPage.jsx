import React, {useEffect, useState} from "react"
import {withRouter} from "react-router"
import {api} from "../api/api"


const CheckConfirm = (props) => {
  const [msg, setMsg] = useState('Check your email, please')
  const [token] = useState(props.match.params.token)


  useEffect(() => {

    const run = async () => {
      const data = await api.confirm(token)
      if (data?.token){

        localStorage.setItem("token", data.token)
        setMsg('Email confirmed!')
      }
      else if (data?.error)
        setMsg('Wrong token!')
    }
    if (token){
      run()
    }

  }, [token])

  return (
    <div>{msg}</div>
  )
}


export default withRouter(CheckConfirm)