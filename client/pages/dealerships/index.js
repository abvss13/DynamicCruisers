import React from 'react'
import Header from '../Header'
import Dealerships from './Dealerships'
import EachDealership from './EachDealership'

function index() {
    return (
        <div>
            <Header />
            <Dealerships />
            <EachDealership />
        </div>
    )
}

export default index