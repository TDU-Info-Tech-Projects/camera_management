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

export const BaseURL = '/api'
// export const BaseURL = 'http://localhost:8000/api'

export const paths = {
    itemRent: BaseURL + "/items/rent",
    itemList: BaseURL + "/items",
    myRentedItems: BaseURL + "/items/rented",
    overdueRentedItems: BaseURL + "/items/overdue",
    returnItem: BaseURL + "/items/return",


    addItem: BaseURL + "/items/add",
    deleteItem: BaseURL + "/items/delete",

    adminUserList: BaseURL + "/admin/users",
    adminRentedItems: BaseURL + "/items/admin/rented",
    adminOverdueRentedItems: BaseURL + "/items/admin/overdue",
    adminReturnItem: BaseURL + "/items/admin/return",

    mountList: BaseURL + "/mounts",
    addMount: BaseURL + "/mounts/add",
    deleteMount: BaseURL + "/mounts/delete",

    authenticate: BaseURL + "/authenticate",
    register: BaseURL + "/register",
    login: BaseURL + "/login",
    logout: BaseURL + "/logout",
}

export const dateStringFormat = (dateStr) => {
    let parsedDate = new Date(dateStr)
    return parsedDate.toISOString().slice(0, 10)
}