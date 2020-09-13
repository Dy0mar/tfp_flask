import {api} from "../api/api";
import {useFormik} from "formik";
import {Button, Form} from "react-bootstrap";
import React, {useState} from "react";
import {Redirect} from "react-router";

const GetAccess = () => {

  const [redirect, setRedirect] = useState(false)

  const  _handleSubmit = async (email) => {
    return await api.get_access(email)
  }

  const validate = values => {
    const errors = {}
    if (!values.email) {
      errors.email = 'Required'
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
      errors.email = 'Invalid email address'
    }

    return errors
  }

  const formik = useFormik({
    initialValues: {
      email: '',
    },
    validate,
    onSubmit: (values, {setSubmitting, setErrors}) => {
      _handleSubmit(values.email).then(r => {
        if (r.error){
          setErrors({email: r.message})
        } else {
          setRedirect(true)
        }
      })
      setSubmitting(false)
    },
  })

  return(
    <div>
      {redirect ? <Redirect to='/confirm' /> : null }

      <h1 className="mt-5">Get access</h1>

      <div className="form-row justify-content-center">
        <Form onSubmit={formik.handleSubmit}>
          <Form.Group controlId="formBasicEmail">

            <Form.Label>Email address</Form.Label>

            <Form.Control required name={'email'} type="email" placeholder="Enter email"
                          onChange={formik.handleChange}  value={formik.values.email} />
            {formik.errors.email ? <div className="text-danger">{formik.errors.email}</div> : null}
            <Form.Text className="text-muted">We'll never share your email with anyone else.</Form.Text>

          </Form.Group>
          <Button variant="primary" type="submit">
            Allow Access
          </Button>
        </Form>
      </div>
    </div>
  )
}

export default GetAccess