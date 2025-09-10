import { makeOutgoingCallApi } from "@/api/outgoingCall.api";
import { CallRequest } from "@/model/call.model";
import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";


interface CallState {
  loading: boolean;
  error: string | null;
  lastResponse: any | null;
}

const initialState: CallState = {
  loading: false,
  error: null,
  lastResponse: null,
};

export const makeOutgoingCall = createAsyncThunk(
  "call/makeCall",
  async (payload: CallRequest, { rejectWithValue }) => {
    try {
      const data = await makeOutgoingCallApi(payload);
      return data;
    } catch (err: any) {
      // try to return readable message
      return rejectWithValue(err?.response?.data || err?.message || "Call failed");
    }
  }
);

const outgoingCallSlice = createSlice({
  name: "outgoingCall",
  initialState,
  reducers: {
    clearCallState(state) {
      state.loading = false;
      state.error = null;
      state.lastResponse = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(makeOutgoingCall.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.lastResponse = null;
      })
      .addCase(makeOutgoingCall.fulfilled, (state, action) => {
        state.loading = false;
        state.lastResponse = action.payload;
      })
      .addCase(makeOutgoingCall.rejected, (state, action) => {
        state.loading = false;
        state.error = (action.payload as any) || "Failed to make call";
      });
  },
});

export const { clearCallState } = outgoingCallSlice.actions;
export default outgoingCallSlice.reducer;
