import {AuthContext} from "../consts/context";
import {AuthProviderProps} from "../model/props";
import {useState} from "react";

export function AuthProvider(props: AuthProviderProps) {
  const [fetchingTokenInProgress, setFetchingTokenInProgress] = useState(true);
  const [userToken, setUserToken] = useState<string | null>(null);

  return (
    <AuthContext.Provider value={{}}>
      {props.children}
    </AuthContext.Provider>
  )
}
