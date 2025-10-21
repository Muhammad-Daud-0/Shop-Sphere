/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from 'react'
import axios from "axios"
import { API_BASE_URL } from '../main'

const useCategory = () => {
    const [categories, setCategories] = useState([])

    const getCategories = async () => {
        try {
            const { data } = await axios.get(`${API_BASE_URL}api/v1/category/get-category`)
            setCategories(data?.categories)
        } catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        getCategories()
    }, [])

    return categories;
}

export default useCategory
