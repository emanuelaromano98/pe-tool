import { createSlice } from '@reduxjs/toolkit'

const initialState = {
    activePage: "theme-search",
    apiKey: ""
}

const mainSlice = createSlice({
    name: "main",
    initialState,
    reducers: {
        setActivePage: (state, action) => {
            state.activePage = action.payload
        },
        setApiKey: (state, action) => {
            state.apiKey = action.payload
        },
        resetApi: (state) => {
            state.activePage = "theme-search"
            state.apiKey = ""
        }
    }
})

export const { setActivePage, setApiKey, resetApi } = mainSlice.actions
export default mainSlice.reducer