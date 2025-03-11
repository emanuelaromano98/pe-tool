import { createSlice } from '@reduxjs/toolkit'

const initialState = {
    activePage: "theme-search",
    apiKey: "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"
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