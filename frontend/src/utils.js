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

export const BaseURL = 'http://localhost:8000/api'
export const paths = {
    itemRent: BaseURL + "/items/rent",
    itemList: BaseURL + "/items",
    myRentedItems: BaseURL + "/items/rented",
    myRentedItems: BaseURL + "/items/rented",
    returnItem: BaseURL + "/items/return",
    
    authenticate: BaseURL + "/authenticate",
    login: BaseURL + "/login",
    logout: BaseURL + "/logout",
}
