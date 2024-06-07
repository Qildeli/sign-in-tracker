import {gql} from "@apollo/client";

export const DASHBOARD_QUERY = gql`
  query Dashboard {
    personalSignInCount
    globalSignInCount
  }
`;
