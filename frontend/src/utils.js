export const httpUtils = {
    post: body => ({
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body),
    }),
    get: () => ({
        method: 'GET',
        credentials: 'include',
    })
}

export const envs = {
  'baseURL': 'http://localhost:8000/api'
}