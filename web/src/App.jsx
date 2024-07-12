import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
// import './App.css'

function App() {
  const [payments, setPayments] = useState([])
  const [users, setUsers] = useState([])

  useEffect(() => {
    fetch('http://127.0.0.1:8000/payment')
      .then((res) => res.json())
      .then((data) => setPayments(data))
    
      fetch('http://127.0.0.1:8000/user')
      .then((res) => res.json())
      .then((data) => setUsers(data))

  },[])

  return (
    <>
      <h1>Autenticación de 2 factores</h1>
      <h2>Transacciones</h2>
      <table className="table table-striped">
        <thead className="thead-dark">
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Nombre</th>
            <th scope="col">Fecha</th>
            <th scope="col">Hora</th>
            <th scope="col">Costo</th>
            <th scope="col">Estado</th>
          </tr>
        </thead>
        <tbody>
          {payments.map((payment) => (
            // <div key={payment.id}>
            <tr>
              <th>{payment.user_id}</th>
              <th>{payment.user_name}</th>
              <th>{payment.date.slice(0,10)}</th>
              <th>{payment.date.slice(11,19)}</th>
              <th>{payment.amount}</th>
              <th style={{
                color: payment.success ? 'green' : 'red'
              }}>{payment.success ? 'Pago Exitoso' : "Pago Fallido"}</th>
            </tr>
            // </div>
          ))}
        </tbody>
      </table>  
      <h2>Saldos</h2>
      <table className="table table-striped">
        <thead className="thead-dark">
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Nombre</th>
            <th scope="col">Dinero (S/)</th>
            <th scope="col">Clave</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            // <div key={payment.id}>
            <tr>
              <th>{user.id}</th>
              <th>{user.name}</th>
              <th>{user.money}</th>
              <th>{user.pin}</th>
            </tr>
            // </div>
          ))}
        </tbody>
      </table>  
    </>
  )
}

export default App
