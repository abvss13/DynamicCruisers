import React from 'react'
import Header from '../Header'
import LeftPane from './LeftPane'
import DashBoardBody from './DashBoardBody'

function index() {
  return (
    <div>
        <Header />
        <div className="dashboard_body">
            <LeftPane />
            <DashBoardBody />
        </div>
    </div>
  )
}

export default index