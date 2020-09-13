import React, {useEffect, useState} from "react"
import {api} from "../api/api"
import UserTable from "./UserTable"


const Home = () => {
  const [users, setUsers] = useState([])
  const [currentUserEmail, setCurrentUserEmail] = useState('')
  const [access, setAccess] = useState(false)
  const [isAdmin, setIsAdmin] = useState(false)

  useEffect(() => {
    const run = async () => {
      const data = await api.get_user_list()
      if (data?.access === true){
        setUsers(data.users)
        setCurrentUserEmail(data.current_user_email)
        setAccess(true)
        setIsAdmin(data.is_admin)
      }
      else {
        setAccess(false)
      }
    }
    run()
  }, [])

  return (
    <div>
      {access
        ? <UserTable users={users} currentUserEmail={currentUserEmail} isAdmin={isAdmin}/>
        : <div >Access denied</div>}
    </div>
  )
}

export default Home