import React, { useState, useEffect, useCallback } from 'react'


const useFetch = (url, options) => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(null)
  const [error, setError] = useState(null)

  const headers = new Headers({
    Accept: 'application/json',
    'Content-Type': 'application/json',
  })

  useEffect(() => {
    setLoading(true)
    setData(null)
    setError(null)

    fetch('http://localhost:8000/apiv1/' + url, { ...options, headers })
      .then((res) => res.json())
      .then((json) => {
        setLoading(false)

        setData(json)
      })
      .catch((err) => {
        setLoading(false)
        setError('An error occurred, details: ' + err)
      })
    return () => { }
  }, [url])
  return { data, loading, error }
}

const useAPI = (url, options = {}, method) => {
  const [response, setResponse] = useState(null)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(null)
  const [error, setError] = useState(null)

  const headers = new Headers({
    Accept: 'application/json',
    'Content-Type': 'application/json',
  })

  const callAPI = useCallback(
    (payload) => {
      setLoading(true)
      setData(null)
      setError(null)

      fetch('http://localhost:8000/apiv1/' + url, { ...options, headers, body: JSON.stringify(payload), method })
        .then((res) => res.json())
        .then((json) => {
          setLoading(false)
          setData(json)
        })
        .catch((err) => {
          setLoading(false)
          setError('An error occurred. Awkward..')
        })
      return () => { }
    },
    [url, headers]
  )
  return { data, loading, error, callAPI }
}

const usePost = (url, options = {}) => useAPI(url, options, 'POST')

const usePatch = (url, options = {}) => useAPI(url, options, 'PATCH')

const useDelete = (url, options = {}) => useAPI(url, options, 'DELETE')

const useFetchAPI = (url, options = {}) => useAPI(url, options, 'GET')

export { useFetch, usePost, usePatch, useDelete, useFetchAPI }