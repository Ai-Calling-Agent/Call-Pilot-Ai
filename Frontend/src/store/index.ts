import { configureStore } from "@reduxjs/toolkit";
import outGoingCallSlice from "./slices/outgoingCallSlice";



export const store = configureStore({
  reducer: {
  outgoingCall: outGoingCallSlice 
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type RootDispatch = typeof store.dispatch;