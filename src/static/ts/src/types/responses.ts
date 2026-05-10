export interface DefaultResponse {
  code: string;
  message: string;
}

export interface ResponseWithData<T> extends DefaultResponse {
  data: T;
}

export interface ResponseWithRedirect extends DefaultResponse {
  redirect_to: string;
}

export type ResponseDirect<T> = T;
