
import { CallRequest } from "@/model/call.model";
import axiosSetup from "@/utils/axiosSetup";

export const makeOutgoingCallApi = async (payload: CallRequest) => {
  try {
    const response = await axiosSetup.post("/call", payload);
    return response.data;
  } catch (error) {
    console.error("makeOutgoingCallApi error:", error);
    throw error;
  }
};